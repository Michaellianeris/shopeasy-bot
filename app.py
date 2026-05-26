"""
ShopEasy Customer Service Bot — FastAPI Web Server
Run with: uvicorn app:app --reload
Visit:    http://localhost:8000
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio
import json

from shopeasy_bot.bot import CustomerServiceBot

app = FastAPI(title="ShopEasy Customer Service Bot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError("Please set the ANTHROPIC_API_KEY environment variable.")

bot = CustomerServiceBot(api_key=api_key)


# ── Request / Response models ─────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    intent: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    intent: str

class ResetResponse(BaseModel):
    status: str

class SummaryResponse(BaseModel):
    summary: str


# ── API routes ────────────────────────────────────────────────────────────────

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Send a message and get a response with intent classification."""
    try:
        intent = bot.classify_intent(req.message)
        reply  = bot.generate_response(req.message, intent=intent)
        return ChatResponse(reply=reply, intent=intent)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset", response_model=ResetResponse)
async def reset():
    """Reset the conversation for a new customer session."""
    bot.reset_conversation()
    return ResetResponse(status="Conversation reset successfully.")


@app.get("/summary", response_model=SummaryResponse)
async def summary():
    """Get a handoff summary of the current conversation."""
    try:
        text = bot.get_conversation_summary()
        return SummaryResponse(summary=text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "model": bot.model}


# ── Serve the frontend ────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
