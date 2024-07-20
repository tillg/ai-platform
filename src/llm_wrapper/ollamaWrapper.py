
from typing import Dict, Union
from ollama import Client
from ai_commons.constants import OLLAMA_BASE_URL, LLM_WRAPPER_DEFAULT_MODEL
import logging
from ai_commons.apiModelsChat import ChatRequest, ChatResponse
from copy import deepcopy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_models_as_json_array():
    logger = logging.getLogger(__name__)
    client = Client(host=OLLAMA_BASE_URL)
    try:
        models = client.list()["models"]
    except Exception as e:
        logger.error(f"Error: {e}")
        return None
    return models

def get_models():
    logger = logging.getLogger(__name__)    
    models_as_json = get_models_as_json_array()
    if models_as_json is None:
        logger.error("Error: Could not get models")
        return None
    model_names = [model['name'] for model in models_as_json]
    return model_names

def get_default_model():
    if LLM_WRAPPER_DEFAULT_MODEL in get_models():
        return LLM_WRAPPER_DEFAULT_MODEL
    return get_models()[0]

def chat(chat_request: ChatRequest) -> ChatResponse:
    client = Client(host=OLLAMA_BASE_URL)
    logger.info(f"Chat req: {chat_request}")
    chat_request = check_and_fix_model_in_request(chat_request)
    logger.info(f"Chat req after check: {chat_request}")
    ollama_response = None
    ollama_messages = chat_request.to_dict()['messages']
    try:
        ollama_response = client.chat(
            messages=ollama_messages, model=chat_request.model)
    except Exception as e:
        logger.error(f"Error: {e}")
        return ChatResponse(content="Error: Could not chat")
    logger.info(f"OLLAMA response: {ollama_response}")
    return ChatResponse(content=ollama_response['message']['content'])

def check_model_exists(model_name: str) -> bool:
    return model_name in get_models()


def check_and_fix_model_in_request(chat_request: ChatRequest) -> ChatRequest:
  
    default_model = get_default_model()

    if (chat_request.model is None) or (not check_model_exists(chat_request.model)):
        logger.info(f"Model not specified, using default model: {
                    default_model}")
        # Create a deep copy of the original request to preserve all other fields
        updated_chat_request = deepcopy(chat_request)
        # Set the model to the default model
        updated_chat_request.model = default_model
        return updated_chat_request
    else:
        # If model is specified, return the original request
        return chat_request
