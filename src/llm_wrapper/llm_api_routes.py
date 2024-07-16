from typing import Any, Dict, Optional, List
import fastapi
from fastapi import Depends, FastAPI, Query, Request, Body, HTTPException
import logging
from ai_commons.apiModelsChat import ChatRequest, ChatResponse
from llm_wrapper import ollamaWrapper

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = fastapi.APIRouter()


@router.get("/")
async def root():
    return {"message": "This is the LLM Wrapper Service! 🧠"}


@router.get("/models")
async def info() -> List[str]:
    return ollamaWrapper.get_models()


@router.post("/chat")
async def chat(chat_request: ChatRequest) -> ChatResponse:
    return ollamaWrapper.chat(chat_request)

