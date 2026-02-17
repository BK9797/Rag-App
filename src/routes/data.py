from fastapi import APIRouter, Depends, UploadFile , File, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
import aiofiles
import os
from models import ResponseSignal
import logging

logger =logging.getLogger("uvicorn.error")
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile = File(...),
                      app_settings : Settings = Depends(get_settings)):
    
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

    file_path, new_filename = DataController().generate_unique_filepath(
    orig_file_name=file.filename,
    project_id=project_id
    )


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
            "signal" : ResponseSignal.FILE_UPLOAD_SUCCESS.value
            }
        )