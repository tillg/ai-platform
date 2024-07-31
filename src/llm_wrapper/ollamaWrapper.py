
from typing import Dict, List, Union
from ollama import Client
from ai_commons.constants import OLLAMA_BASE_URL, LLM_WRAPPER_DEFAULT_MODEL
import logging
from ai_commons.apiModelsChat import ChatRequest, ChatResponse
from ai_commons.apiModelsLlm import Model
from copy import deepcopy
from utils.simplify_dict import ensure_str_str_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_models_as_json_array(client):
    logger = logging.getLogger(__name__)
    try:
        models = client.list()["models"]
    except Exception as e:
        logger.error(f"Error: {e}")
        return None
    return models


def get_running_models_as_json(client):
    logger = logging.getLogger(__name__)
    try:
        running_models = client.ps()["models"]
    except Exception as e:
        logger.error(f"Error: {e}")
        return None
    return running_models


def get_models() -> List[Model]:
    logger = logging.getLogger(__name__)
    client = Client(host=OLLAMA_BASE_URL)
    models_as_json = get_models_as_json_array(client)
    if models_as_json is None:
        logger.error("Error: Could not get models")
        return None
    running = get_running_models_as_json(client)
    models = []
    for model in models_as_json:
        description = f"Family: {model["details"]["family"]}, Size: {model["details"]["parameter_size"]}"
        details = ensure_str_str_dict(model)
        state = None
        if model["name"] in running:
            state = "Running"
        models.append(
            Model(name=model['name'], description=description, details=details, state=state))
    return models

def get_default_model() -> Model:
    if LLM_WRAPPER_DEFAULT_MODEL in get_models():
        return get_models()[LLM_WRAPPER_DEFAULT_MODEL]
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
  
    default_model_name = get_default_model().name

    if (chat_request.model is None) or (not check_model_exists(chat_request.model)):
        logger.info(f"Model not specified, using default model: {
                    default_model_name}")
        # Create a deep copy of the original request to preserve all other fields
        updated_chat_request = deepcopy(chat_request)
        # Set the model to the default model
        updated_chat_request.model = default_model_name
        return updated_chat_request
    else:
        # If model is specified, return the original request
        return chat_request
