from fastapi import APIRouter, Depends, UploadFile , File, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
import aiofiles
import os
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk

logger =logging.getLogger("uvicorn.error")
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file: UploadFile = File(...),
                      app_settings : Settings = Depends(get_settings)):
    
    project_model = ProjectModel(db_client=request.app.db_client)

    project = await project_model.get_project_or_create_one(project_id=project_id)
    
    data_Controller = DataController()

    is_valid ,result  = data_Controller.validate_uploaded_file(file)
    if not is_valid:
        return JSONResponse(
                        status_code = status.HTTP_400_BAD_REQUEST ,
                        content = {
                            "signal" : result
                            }
                        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)

    file_path ,file_id  = DataController().generate_unique_filepath(orig_file_name=file.filename , project_id= project_id)


    try:
        # save file as chunckes at hard rather than download full file in temp memory (RAM)
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE) :
                await f.write(chunk) 

    except Exception as e :
        # save error in logger to handel clinet problem 
        logger.error(f"Error while uploading file: {e}")

        # show faild message only for user but the error message appear in log file for admin
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST ,
            content = {
                "signal" : ResponseSignal.FILE_UPLOAD_FAILED.value,
                }
            )

    return JSONResponse(
        status_code = status.HTTP_200_OK ,
        content = {
            "signal" : ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id" : file_id,
            }

        )

@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id : str , process_request : ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model = ProjectModel(db_client=request.app.db_client)

    project = await project_model.get_project_or_create_one(project_id=project_id)

    process_controller = ProcessController(project_id=project_id)

    file_content = process_controller.get_file_content(file_id=file_id)

    file_chunks = process_controller.process_file_content(file_content=file_content,file_id=file_id, chunk_size=chunk_size, overlap_size=overlap_size)

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST ,
            content = {
                "signal" : ResponseSignal.PROCESSING_FAILD.value,
                }
            )

    file_chunks_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i + 1,
            chunk_project_id=project.id
        )
        for i, chunk in enumerate(file_chunks)
    ]

    Chunk_model = ChunkModel(db_client=request.app.db_client)
    if do_reset == 1:
        _ = await Chunk_model.delete_chunks_by_project_id(project_id=project.id)

    Chunk_model = ChunkModel(db_client=request.app.db_client)

    no_records = await Chunk_model.insert_many_chunks(chunks=file_chunks_records)

    return JSONResponse(
        status_code = status.HTTP_200_OK ,
        content = {
            "signal" : ResponseSignal.PROCESSING_SUCESS.value,
            "inserted_chunks" : no_records
            }
    )