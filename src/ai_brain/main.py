from fastapi import Depends, FastAPI, Query
import uvicorn

import ai_brain.api_routes
import logging
import ai_commons.constants as constants
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from ai_brain.brain import Brain

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

AI_BRAIN_PORT = os.environ.get('AI_BRAIN_PORT', 8081)
AI_BRAINS_DIRECTORY = os.environ.get('AI_BRAINS_DIRECTORY', 'data/brains')

logger.info(f"Brains directory: {AI_BRAINS_DIRECTORY}")

app = FastAPI()
allowed_origins = ["*"]
# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(ai_brain.api_routes.router)

brain: Brain = Brain()

if __name__ == "__main__":
    uvicorn.run("ai_brain.main:app",
                host="0.0.0.0", port=AI_BRAIN_PORT, reload=True)
