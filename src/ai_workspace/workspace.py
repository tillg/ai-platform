import logging
from typing import Optional
import uuid
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
import chromadb
from chromadb.config import Settings
from ai_workspace.constants import COLLECTION_NAME, VECTORESTORE_DIRECTORY
from ai_commons.api_models import Document


class Workspace:

    def __init__(
        self,
        vectore_store_directory: Optional[str] = VECTORESTORE_DIRECTORY,
        collection_name: Optional[str] = COLLECTION_NAME,
    ):
        self.chroma_collection = _get_chroma_collection(
            vectore_store_directory, collection_name)

    def search(
        self,
        query: str | None,
        n: int = 5,
    ) -> list[Document] | None:
        log = logging.getLogger(__name__)
        results = self.chroma_collection.query(
            query_texts=[query],
            n_results=n
        )
        log.info(f"Search results: {results}")
        return results

    def add_documents(self, documents: list[Document]):
        log = logging.getLogger(__name__)
        for document in documents:
            if document.id is None:
                # str(uuid.uuid4())
                document.id = str(uuid.uuid5(
                    uuid.NAMESPACE_DNS, document.source))
        ids = [doc.id for doc in documents]
        chroma_documents = [doc.content for doc in documents]
        metadatas = [{**doc.metadata, 'source': doc.source}
                     if doc.source is not None else doc.metadata for doc in documents]
        try:
            self.chroma_collection.add(
                ids=ids, documents=chroma_documents, metadatas=metadatas)
        except Exception as e:
            log.error(f"Error adding documents to collection: {e}")
            raise e


def _get_chroma_collection(vectore_store_directory: str, collection_name: str):

    # create EF with custom endpoint
    ef = OllamaEmbeddingFunction(
        model_name="nomic-embed-text",
        url="http://localhost:11434/api/embeddings",
    )

    client = chromadb.PersistentClient(
        path=vectore_store_directory,
        settings=Settings(
            anonymized_telemetry=False, is_persistent=True, )

    )
    collection = client.get_or_create_collection(collection_name,
                                                 embedding_function=ef,)
    return collection
