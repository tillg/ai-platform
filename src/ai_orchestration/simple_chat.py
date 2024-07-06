from ai_commons.apiModelsChat import ChatRequest, ChatResponse
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class SimpleChat:
    def run(self, chat_request: ChatRequest, options: dict = {}) -> ChatResponse:
        logger.info(f"Running SimpleChat with {chat_request}")
        chat_response = ChatResponse(content="Hello World")
        return chat_response

