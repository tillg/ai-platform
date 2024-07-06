import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
import uvicorn

import ai_orchestration.api_routes
import logging
import ai_commons.constants as constants
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

AI_CHAT_PORT = os.environ.get('AI_CHAT_PORT', 8001)

logger.info(f"Chat port: {AI_CHAT_PORT}")


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

app.include_router(ai_orchestration.api_routes.router)



if __name__ == "__main__":
    uvicorn.run("ai_orchestration.main:app",
                host="0.0.0.0", port=AI_CHAT_PORT, reload=True)
