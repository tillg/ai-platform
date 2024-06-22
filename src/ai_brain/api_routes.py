import fastapi
from ai_orchestration.rag_chain import RagChain
from ai_commons.api_models import ChatRequest, ChatResponse

router = fastapi.APIRouter()



@router.post("/chat")
async def chat_handler(chat_request: ChatRequest) -> ChatResponse:
    messages = [message.model_dump() for message in chat_request.messages]
    overrides = chat_request.context.get("overrides", {})

    

    # response = await ragchat.run(messages, overrides=overrides)
    response = None
    return response
