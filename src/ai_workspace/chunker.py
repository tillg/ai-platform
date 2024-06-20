from langchain.docstore.document import Document as lc_Document
from ai_commons.api_models import Document, Chunk
from langchain.text_splitter import CharacterTextSplitter
from typing import List
from dotenv import load_dotenv
import logging
from utils.robust_jsonify import robust_jsonify
import os
import uuid

load_dotenv()
logger = logging.getLogger(__name__)

CHUNKER_SEPARATOR = os.environ.get('CHUNKER_SEPARATOR', "\n\n")
CHUNKER_CHUNK_SIZE = os.environ.get('CHUNKER_CHUNK_SIZE', 256)
CHUNKER_CHUNK_OVERLAP = os.environ.get('CHUNKER_CHUNK_OVERLAP', 20)


class Chunker:

    def __init__(self, separator: str = CHUNKER_SEPARATOR, chunk_size: int = CHUNKER_CHUNK_SIZE, chunk_overlap: int = CHUNKER_CHUNK_OVERLAP):
        logger.info(f"Chunker initialized with separator: {
                    separator}, chunk_size: {chunk_size}, chunk_overlap: {chunk_overlap}")
        self.text_splitter = CharacterTextSplitter(
            separator=separator,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

    def chunkify(self, document: Document) -> List[Document]:
        if not isinstance(document, Document):
            logger.error(
                f"document is not an instance of Document: {document}. It is of type {type(document)}")
            raise TypeError(
                f"document must be an instance of Document, not {type(document)}")
        lc_document = document.to_lc_document()
        try:
            lc_chunks = self.text_splitter.create_documents(
                [document.page_content], metadatas=[lc_document.metadata])
        except Exception as e:
            logger.error(
                f"Error while chunkifying document: {robust_jsonify(document)}")
            logger.error(f"Error: {e}")
            raise
        chunks = []
        for lc_chunk in lc_chunks:
            chunk = Chunk(
                page_content=lc_chunk.page_content, 
                title=lc_chunk.metadata.get("title", None), 
                uri=lc_chunk.metadata.get("uri", None), 
                original_document_id=document.id
            )
            chunks.append(chunk)
        logger.debug(f"Chunkified in chunks of length: {
            [len(chunk.page_content) for chunk in chunks]}")
        return chunks

    def chunkify_documents(self, documents: List[Document]) -> List[Document]:
        if not isinstance(documents, list):
            logger.error(
                f"documents is not a list: {documents}. It is of type {type(documents)}")
            raise TypeError(f"documents must be a list, not {type(documents)}")
        if not all(isinstance(doc, Document) for doc in documents):
            logger.error(
                f"All elements in list are not instances of Document.")
            raise TypeError(
                "All elements in documents must be instances of Document")

        # chunks = [self.chunkify_document(document) for document in documents]
        chunks = [
            chunk for document in documents for chunk in self.chunkify_document(document)]

        return chunks
