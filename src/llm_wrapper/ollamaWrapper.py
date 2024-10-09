
from typing import Dict, List, Union
from ollama import Client as OllamaClient
from ai_commons.constants import OLLAMA_BASE_URL, LLM_WRAPPER_DEFAULT_MODEL, OLLAMA_KEEP_ALIVE, OLLAMA_DEFAULT_TEMPERATURE
import logging
from ai_commons.apiModelsChat import ChatRequest, Message
from ai_commons.apiModelsLlm import Model
from copy import deepcopy
from utils.simplify_dict import ensure_str_str_dict

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

def get_models_as_json_array(client):
    logger = logging.getLogger(__name__)
    try:
        models = client.list()["models"]
    except Exception as e:
        logger.error(f"get_models_as_json_array {e}")
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
    client = OllamaClient(host=OLLAMA_BASE_URL)
    models_as_json = get_models_as_json_array(client)
    if models_as_json is None:
        logger.error("Error: Could not get models")
        return [] 
    running = get_running_models_as_json(client)
    models = []
    for model in models_as_json:
        description = f"Family: {model["details"]["family"]}, Size: {model["details"]["parameter_size"]}"
        details = ensure_str_str_dict(model)
        state = None
        if model["name"] in running:
            state = "Running"
        default = False
        if model["name"] == LLM_WRAPPER_DEFAULT_MODEL:
            default = True
        models.append(
            Model(name=model['name'], description=description, details=details, state=state, default=default))
    return models

def get_model_names() -> List[str]:
    models = get_models()
    return [model.name for model in models]

def get_default_model_name() -> str:
    if LLM_WRAPPER_DEFAULT_MODEL in get_model_names():
        return LLM_WRAPPER_DEFAULT_MODEL
    return get_models()[0].name

def extract_inner_working(ollama_response: Dict[str, Union[str, int]]) -> Dict[str, Union[str, int]]:
    ollama_fields_to_report = ["model", "total_duration",
                               "prompt_eval_count", "eval_count", "load_duration", "prompt_eval_duration", "eval_duration"]
    inner_working = {}
    for field in ollama_fields_to_report:
        if field in ollama_response:
            inner_working[field] = ollama_response.get(field, None)
    return inner_working

def chat(chat_request: ChatRequest) -> Message:
    client = OllamaClient(host=OLLAMA_BASE_URL)
    logger.info(f"Chat req: {chat_request}")
    chat_request = check_and_fix_model_in_request(chat_request)
    logger.info(f"Chat req after check: {chat_request}")
    ollama_response = None
    ollama_messages = chat_request.to_dict()['messages']
    if chat_request.options is None:
        temp = OLLAMA_DEFAULT_TEMPERATURE
    else:
        temp = chat_request.options.get('temperature', OLLAMA_DEFAULT_TEMPERATURE)
    ollama_options={'temperature': temp}
    try:
        ollama_response = client.chat(
            messages=ollama_messages, model=chat_request.model, options=ollama_options, keep_alive=OLLAMA_KEEP_ALIVE)
    except Exception as e:
        logger.error(f"Error: {e}")
        return Message(content="Error: Could not chat")
    logger.info(f"OLLAMA response: {ollama_response}")
    inner_working = extract_inner_working(ollama_response)
    inner_working["temperature"] = temp
    return Message(content=ollama_response['message']['content'], role="assistant", inner_working=inner_working)


def check_model_exists(model_name: str) -> bool:
    return model_name in get_model_names()


def check_and_fix_model_in_request(chat_request: ChatRequest) -> ChatRequest:
  
    default_model_name = get_default_model_name()

    if (chat_request.model is None) or (not check_model_exists(chat_request.model)):
        logger.info(f"Model not specified ({chat_request.model}), using default model: {
                    default_model_name}")
        # Create a deep copy of the original request to preserve all other fields
        updated_chat_request = deepcopy(chat_request)
        # Set the model to the default model
        updated_chat_request.model = default_model_name
        return updated_chat_request
    else:
        # If model is specified, return the original request
        return chat_request

