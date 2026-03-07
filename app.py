import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from agent import MFTAgent

app = FastAPI(title="MFT Operations Agent")
agent = MFTAgent()

app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    print(f"User: {request.message}")
    response = agent.chat(request.message)
    print(f"Agent: {response}")
    return ChatResponse(response=response)


@app.post("/reset")
async def reset():
    agent.reset()
    return {"status": "Conversation cleared"}


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=False)