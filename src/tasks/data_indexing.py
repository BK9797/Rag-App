import logging
from uuid import uuid4
from stores.llm.LLMEnums import DocumentTypeEnum
from models.db_schemes import DataChunk
from models.enums.DataBaseEnum import DataBaseEnum

logger = logging.getLogger(__name__)


class AsyncTask:
    """Mock async task for development without Celery/Redis"""
    def __init__(self, task_id=None):
        self.id = task_id or str(uuid4())
        self.status = "pending"
        self.result = None


async def index_data_content_async(project_id: int, do_reset: bool,
                                    db_client, embedding_client, vectordb_client):
    """
    Async implementation to index data content into vector database.
    
    Uses the app's existing MongoDB, embedding, and vector DB clients
    to fetch chunks, generate embeddings, and insert them into Qdrant.
    
    Args:
        project_id: The project ID to index
        do_reset: Whether to reset the existing index
        db_client: The app's MongoDB database client
        embedding_client: The app's embedding client
        vectordb_client: The app's vector DB client
    
    Returns:
        Task result with status
    """
    try:
        logger.info(f"Starting data indexing for project {project_id}, reset={do_reset}")

        # Build collection name
        collection_name = f"collection_{vectordb_client.default_vector_size}_{project_id}".strip()

        # First, find the project to get its ObjectId
        project_collection = db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
        project_doc = await project_collection.find_one({"project_id": str(project_id)})

        if not project_doc:
            logger.warning(f"Project {project_id} not found in database")
            return {
                "status": "warning",
                "project_id": project_id,
                "message": f"Project {project_id} not found. Create the project first.",
            }

        project_object_id = project_doc["_id"]
        logger.info(f"Found project ObjectId: {project_object_id}")

        # Fetch chunks using the project's ObjectId (not the string project_id)
        chunk_collection = db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
        cursor = chunk_collection.find({"chunk_project_id": project_object_id})
        raw_chunks = await cursor.to_list(length=None)

        if not raw_chunks or len(raw_chunks) == 0:
            logger.warning(f"No chunks found for project {project_id}")
            return {
                "status": "warning",
                "project_id": project_id,
                "message": f"No chunks found for project {project_id}. Upload and process files first.",
            }

        chunks = [DataChunk(**doc) for doc in raw_chunks]
        logger.info(f"Found {len(chunks)} chunks for project {project_id}")

        # Generate embeddings
        texts = [c.chunk_text for c in chunks]
        metadata = [c.chunk_metadata for c in chunks]
        
        vectors = []
        for text in texts:
            embedded = embedding_client.embed_text(
                text=text,
                document_type=DocumentTypeEnum.DOCUMENT.value,
            )
            vectors.append(embedded[0])

        # Create collection (reset if requested)
        vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=embedding_client.embedding_size,
            do_reset=do_reset,
        )

        # Generate chunk IDs (sequential integers)
        chunks_ids = list(range(1, len(chunks) + 1))

        # Insert into vector DB
        vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            metadata=metadata,
            vectors=vectors,
            record_ids=chunks_ids,
        )

        result = {
            "status": "success",
            "project_id": project_id,
            "indexed_chunks": len(chunks),
            "collection_name": collection_name,
            "message": f"Data indexing completed for project {project_id}: {len(chunks)} chunks indexed",
        }

        logger.info(result["message"])
        return result

    except Exception as e:
        logger.error(f"Error indexing data for project {project_id}: {str(e)}")
        return {
            "status": "error",
            "project_id": project_id,
            "error": str(e),
        }
