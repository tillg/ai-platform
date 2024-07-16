from fastapi import Depends, FastAPI, Query
import uvicorn
import ai_brain.brain_api_routes
import logging
import ai_commons.constants as constants
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from ai_brain.brain import Brain

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

AI_BRAIN_PORT = constants.AI_BRAIN_PORT

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

app.include_router(ai_brain.brain_api_routes.router)

def start_ai_brain(reload = False):
   uvicorn.run("ai_brain.main:app",
               host="0.0.0.0", port=AI_BRAIN_PORT, reload=reload)
   
if __name__ == "__main__":
   start_ai_brain(reload=True) 
