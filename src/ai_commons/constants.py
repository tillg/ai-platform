import os
from utils.utils import find_project_root

AI_ORCHESTRATION_PORT = 8003
AI_LLM_WRAPPER_PORT = 8002
AI_BRAIN_PORT = 8001

OLLAMA_BASE_URL = "http://localhost:11434"

CHAT_BACKEND_URL = "http://localhost"

PROJECT_ROOT = find_project_root(os.path.abspath(__file__))
DATA_DIRECTORY = os.path.join(PROJECT_ROOT, "data")

AI_BRAINS_DIRECTORY = os.path.join(DATA_DIRECTORY, "brains")  
AI_BRAIN_COLLECTION_NAME = 'COLLECTION_NAME'



