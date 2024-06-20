from typing import Any, Optional
import uuid
from pydantic import BaseModel
from langchain.docstore.document import Document as lc_Document


class Message(BaseModel):
    content: str
    role: str = "user"


class Document(BaseModel):
    title: str
    content: str
    uri: str
    id: uuid.UUID = None  # Set default to None

    def __init__(self, **data):
        if 'id' not in data or data['id'] is None:
            data['id'] = uuid.uuid4()
        super().__init__(**data)    

    @classmethod
    def from_lc_document(cls, lc_document: lc_Document) -> 'Document':
        return Document(
            title=lc_document.metadata.get("title", None),
            content=lc_document.page_content,
            uri=lc_document.metadata.get("source", None)
        )

    def to_lc_document(self) -> lc_Document:
        return lc_Document(
            page_content=self.content,
            metadata={"source": self.uri, "title": self.title,
                      "id": self.id if hasattr(self, 'id') else None}
        )


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
