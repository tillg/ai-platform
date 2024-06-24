from typing import Any, Optional
import uuid
from pydantic import BaseModel
from langchain.docstore.document import Document as lc_Document
import os
from utils.dict2file import write_dict_to_file, read_dict_from_file


class Message(BaseModel):
    content: str
    role: str = "user"


class SearchRequest(BaseModel):
    search_term: str


class Document(BaseModel):
    title: str
    content: str
    uri: str
    id: str = None  # Set default to None

    def __init__(self, **data):
        if 'id' not in data or data['id'] is None:
            data['id'] = str(uuid.uuid4())
        super().__init__(**data)

    @classmethod
    def from_lc_document(cls, lc_document: lc_Document) -> 'Document':
        return Document(
            title=lc_document.metadata.get("title", None),
            content=lc_document.page_content,
            uri=lc_document.metadata.get("source", None),
            id=lc_document.metadata.get("id", str(uuid.uuid4()))
        )

    @classmethod
    def from_text_file(cls, file_path: str) -> 'Document':
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        title = os.path.splitext(os.path.basename(file_path))[0]
        return Document(title=title, content=content, uri=file_path)

    @classmethod
    def get_filename_by_id(cls, directory: str, id: str, prefix: str = None):
        if prefix:
            return os.path.join(directory,  prefix + "_" + id + ".json")
        return os.path.join(directory,  id + ".json")

    def to_lc_document(self) -> lc_Document:
        return lc_Document(
            page_content=self.content,
            metadata=self.get_metadata()
        )

    def get_metadata(self) -> dict:
        doc_dict = self.model_dump()
        del doc_dict["content"]
        return doc_dict

    def write_2_file(self, directory: str):
        filename = Document.get_filename_by_id(directory, self.id)
        if hasattr(self, 'search_info'):
            prefix = f"{self.search_info.distance:07.5f}"
            filename = Document.get_filename_by_id(
                directory, self.id, prefix=prefix)
        document_dict = self.model_dump()

        # Write to file
        write_dict_to_file(dictionary=document_dict, full_filename=filename)
        return


class SearchInfo(BaseModel):
    search_term: str
    distance: float


class Chunk(Document):
    original_document_id: str
    search_info: Optional[SearchInfo] = None

    @classmethod
    def chroma_chunks2chunk_array(cls, chroma_chunks, search_term: str = None) -> list['Chunk']:
        chunks = []
        for counter, id in enumerate(chroma_chunks['ids'][0]):
            chunk = Chunk(
                title=chroma_chunks['metadatas'][0][counter].get(
                    "title", None),
                uri=chroma_chunks['metadatas'][0][counter].get("uri", None),
                content=chroma_chunks['documents'][0][counter],
                id=id,
                original_document_id=chroma_chunks['metadatas'][0][counter].get(
                    "original_document_id", None)
            )
            if search_term:
                search_info = SearchInfo(
                    search_term=search_term, distance=chroma_chunks['distances'][0][counter])
                chunk.search_info = search_info
            chunks.append(chunk)
        return chunks


class SearchResult(BaseModel):
    chunks: list[Chunk]
    
class ChatRequest(BaseModel):
    messages: list[Message]
    context: dict = {}


class ChatResponse(BaseModel):
    message: str


class ThoughtStep(BaseModel):
    title: str
    description: Any
    props: dict = {}
