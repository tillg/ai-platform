from fastapi import Depends, FastAPI
import uvicorn

import ai_orchestration.api_routes
import logging
import ai_commons.constants as constants

logging.basicConfig(level=logging.INFO)


app = FastAPI()

app.include_router(ai_orchestration.api_routes.router)
# app.mount("/", frontend_routes.router)


@app.get("/")
async def root():
    return {"message": "This is the AI Orchestration Service!"}


if __name__ == "__main__":
    uvicorn.run("ai_orchestration.main:app",
                host="0.0.0.0", port=constants.AI_ORCHESTRATION_PORT, reload=True)
