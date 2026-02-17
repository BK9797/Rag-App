from enum import Enum

class ResponseSignal(Enum):
   FILE_VALIDATED_SUCCESS = "FILE_VALIDATED_SUCCESS"
   FILE_TYPE_NOT_SUPPORTED = "FILE_TYPE_NOT_SUPPORTED"
   FILE_SIZE_TOO_LARGE = "FILE_SIZE_TOO_LARGE"
   FILE_UPLOAD_SUCCESS = "FILE_UPLOAD_SUCCESS"
   FILE_UPLOAD_FAILED = "FILE_UPLOAD_FAILED"
   
   PROCESSING_SUCESS = "processing_sucesss"
   PROCESSING_FAILD = "processing faild"

   NO_FILES_ERROR = "not found files"
   FILE_ID_ERROR = "no file found with this id"

   PROJECT_NOT_FOUND_ERROR = "project_not_found"
   INSERT_INTO_VECTORDB_EROOR ="insert_into_vectordb_error"
   INSERT_INTO_VECTORDB_SUCCESS ="insert_into_vectordb_success"

   VECTOR_BD_COLLECTION_RETIVED = "vectordb collection retrived"
   VECTORDB_SEARCH_SUCCESS = "vectordb search sucsses"
   VECTORDB_SEARCH_ERROR = "vectordb search error"

   RAG_ANSWER_ERROR = "rag answer error"
   RAG_ANSWER_SUCCESS = "rag answer success"
