import os
from utils.utils import find_project_root

AI_ORCHESTRATION_HOST = "localhost"
AI_ORCHESTRATION_PORT = 8003

AI_LLM_WRAPPER_HOST = "localhost"
AI_LLM_WRAPPER_PORT = 8002

AI_BRAIN_HOST = "localhost"
AI_BRAIN_PORT = 8001

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_KEEP_ALIVE = "8h"
OLLAMA_DEFAULT_TEMPERATURE = 0.8  # 0.8 is the default

CHAT_BACKEND_URL = "http://localhost"

PROJECT_ROOT = find_project_root(os.path.abspath(__file__))
DATA_DIRECTORY = os.path.join(PROJECT_ROOT, "data")

AI_BRAINS_INDEX_FILE = os.path.join(DATA_DIRECTORY, "brains/brains.json")
AI_BRAIN_COLLECTION_NAME = 'COLLECTION_NAME'

LLM_WRAPPER_DEFAULT_MODEL = "mixtral:8x7b-instruct-v0.1-q8_0"

CHUNKER_SEPARATOR = '\n'
CHUNKER_CHUNK_SIZE = 256
CHUNKER_CHUNK_OVERLAP = 20

# in relation to this file my test data resides in ../../data/test_data
TEST_DATA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "data", "test_data")
TMP_DATA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "data", "tmp")


EMBEDDING_MODEL = "nomic-embed-text"
COLLECTION_NAME = "collection"
VECTORESTORE_DIRECTORY = "../data/vectorestores"
OLLAMA_BASE_URL = "http://localhost:11434"
