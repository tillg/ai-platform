from typing import Any, Optional
import uuid
from pydantic import BaseModel
from langchain.docstore.document import Document as lc_Document
import os

class Message(BaseModel):
    content: str
    role: str = "user"


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

    def to_lc_document(self) -> lc_Document:
        return lc_Document(
            page_content=self.content,
            metadata=self.get_metadata()
        )
    
    def get_metadata(self) -> dict:
        doc_dict = self.model_dump()
        del doc_dict["content"]
        return doc_dict


class Chunk(Document):
    original_document_id: str


class ChatRequest(BaseModel):
    messages: list[Message]
    context: dict = {}


class ChatResponse(BaseModel):
    message: str


class ThoughtStep(BaseModel):
    title: str
    description: Any
    props: dict = {}
