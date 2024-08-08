from typing import Any, Dict, Optional, List
import fastapi
import logging
from ai_commons.apiModelsChat import ChatRequest, Message
from ai_commons.apiModelsLlm import Model
from llm_wrapper import ollamaWrapper

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = fastapi.APIRouter()

@router.get("/")
async def root():
    return {"message": "This is the LLM Wrapper Service! 🧠"}

@router.get("/models")
async def info() -> List[Model]:
    return ollamaWrapper.get_models()

@router.post("/chat")
async def chat(chat_request: ChatRequest) -> Message:
    return ollamaWrapper.chat(chat_request)

