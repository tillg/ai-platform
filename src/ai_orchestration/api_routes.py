import fastapi
from ai_orchestration.rag_chain import RagChain
from ai_commons.apiModelsChat import ChatRequest, ChatResponse
import logging

from ai_orchestration.simple_chat import SimpleChat

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = fastapi.APIRouter()
chat = SimpleChat()

@router.get("/")
async def root():
    return {"message": "This is the AI Orchestration Service! 💬"}

@router.post("/chat")
async def chat_handler(chat_request: ChatRequest) -> ChatResponse:
    # messages = [message.model_dump() for message in chat_request.messages]
    # overrides = chat_request.context.get("overrides", {})
    logger.info(f"Running Chat with {chat_request}")

    response =  chat.run(chat_request)
    return response
