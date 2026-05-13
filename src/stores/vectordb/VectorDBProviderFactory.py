from .providers import QdrantDBProvider
from .VectorDBEnums import VectorDBEnums
from controllers.BaseController import BaseController


class VectorDBProviderFactory:
    def __init__(self, config):
        self.config = config
        self.base_controller = BaseController()

    def create(self, provider):
        # Convert string to enum if needed
        if isinstance(provider, str):
            provider = VectorDBEnums(provider)
        
        if provider == VectorDBEnums.QDRANT:
            db_path = self.base_controller.get_database_path(
                db_name=self.config.VECTOR_DB_PATH
            )

            return QdrantDBProvider(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                default_vector_size=self.config.EMBEDDING_MODEL_SIZE,
                index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD,
            )

        raise ValueError(f"Unsupported vector DB provider: {provider}")