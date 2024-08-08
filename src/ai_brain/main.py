from fastapi import Depends, FastAPI, Query
import uvicorn
import ai_brain.brain_api_routes
import logging
from ai_commons.constants import AI_BRAIN_HOST, AI_BRAIN_PORT
from fastapi.middleware.cors import CORSMiddleware
from ai_brain.brain import Brain

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app = FastAPI(
    title="Brains",
    description="Vector databases with their loading mechanism - we call them brains.",
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

app.include_router(ai_brain.brain_api_routes.router)

def start_ai_brain(reload = False):
   uvicorn.run("ai_brain.main:app",
               host=AI_BRAIN_HOST, port=AI_BRAIN_PORT, reload=reload)
   
if __name__ == "__main__":
   start_ai_brain(reload=True) 
