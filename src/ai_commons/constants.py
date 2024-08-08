import os
from utils.utils import find_project_root

AI_ORCHESTRATION_HOST = "localhost"
AI_ORCHESTRATION_PORT = 8003

AI_LLM_WRAPPER_HOST = "localhost"
AI_LLM_WRAPPER_PORT = 8002

AI_BRAIN_HOST="localhost"
AI_BRAIN_PORT = 8001

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_KEEP_ALIVE = "8h"
OLLAMA_DEFAULT_TEMPERATURE=0.8 # 0.8 is the default

CHAT_BACKEND_URL = "http://localhost"

PROJECT_ROOT = find_project_root(os.path.abspath(__file__))
DATA_DIRECTORY = os.path.join(PROJECT_ROOT, "data")

AI_BRAINS_DIRECTORY = os.path.join(DATA_DIRECTORY, "brains")  
AI_BRAIN_COLLECTION_NAME = 'COLLECTION_NAME'

LLM_WRAPPER_DEFAULT_MODEL = "mixtral:8x7b-instruct-v0.1-q8_0"
