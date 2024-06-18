from typing import Any
from pydantic import BaseModel


class Message(BaseModel):
    content: str
    role: str = "user"

class Document(BaseModel):
    title: str
    content: str
    uri: str

class ChatRequest(BaseModel):
    messages: list[Message]
    context: dict = {}

class ChatResponse(BaseModel):
    message: str

class ThoughtStep(BaseModel):
    title: str
    description: Any
    props: dict = {}

