from fastapi import Depends, FastAPI
import uvicorn

import ai_brain.api_routes
import logging
import ai_commons.constants as constants
from dotenv import load_dotenv
import os

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

AI_BRAIN_PORT = os.environ.get('AI_BRAIN_PORT', 8081)

app = FastAPI()

app.include_router(ai_brain.api_routes.router)


@app.get("/")
async def root():
    return {"message": "This is the AI Brain Service! 🧠"}


if __name__ == "__main__":
    uvicorn.run("ai_brain.main:app",
                host="0.0.0.0", port=AI_BRAIN_PORT, reload=True)
