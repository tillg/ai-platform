
from fastapi import Depends, FastAPI
import uvicorn
from ai_commons.constants import AI_ORCHESTRATION_HOST, AI_ORCHESTRATION_PORT
import ai_orchestration.api_routes
import logging
import ai_commons.constants as constants
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info(f"Orchestration port: {AI_ORCHESTRATION_PORT}")

app = FastAPI(
    title="AI Orchestration",
    description="Interact with AI chains that combine vector databases and LLMs.",
)
allowed_origins = ["*"]
# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(ai_orchestration.api_routes.router)

def start_ai_orchestration(reload=False):
    uvicorn.run("ai_orchestration.main:app",
                host=AI_ORCHESTRATION_HOST, port=AI_ORCHESTRATION_PORT, reload=reload)

if __name__ == "__main__":
        start_ai_orchestration(reload=True)