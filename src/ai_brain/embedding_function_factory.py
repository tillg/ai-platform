from typing import Any, Dict
from chromadb import Documents, EmbeddingFunction, Embeddings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class EmbeddingFunctionFactory:

    def create_embedding_function(self, parameters: Dict[str, Any]) -> EmbeddingFunction:
        """
        Create an embedding function from the given parameters.
        """
        embedding_function_type = parameters.get(
            "embedding_function_type", "default_embedding_function")
        logger.info(f"Creating embedding function of type {embedding_function_type}")
        if embedding_function_type == "default_embedding_function":
            return DefaultEmbeddingFunction()
        else:
            logger.error(f"Unknown embedding function type: {embedding_function_type}")
            raise ValueError(f"Unknown embedding function type: {embedding_function_type}")
