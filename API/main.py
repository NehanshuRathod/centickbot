from fastapi import FastAPI, Depends, HTTPException, status, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import time

from model_logic import generate_reply

app = FastAPI(title="Chatbot API", version="1.0.0")

# -----------------------------------------------------------
# CORS – allow local frontend
# -----------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in prod, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------
# Simple API key security (optional for now)
# -----------------------------------------------------------
API_KEY = os.getenv("CHATBOT_API_KEY")  # if not set, auth is skipped

async def verify_api_key(x_api_key: str | None = Header(None, alias="X-API-Key")):
    # If no key is configured, don't enforce auth (good for local dev)
    if API_KEY is None:
        return

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )

# -----------------------------------------------------------
# Simple in-memory rate limiter (per IP)
# -----------------------------------------------------------
RATE_LIMIT = 20        # max requests
WINDOW_SECONDS = 60    # per 60 seconds

# ip -> list of timestamps
request_log: Dict[str, List[float]] = {}

async def rate_limiter(request: Request):
    client_ip = request.client.host
    now = time.time()

    timestamps = request_log.get(client_ip, [])
    # keep only timestamps within the current window
    timestamps = [t for t in timestamps if now - t < WINDOW_SECONDS]

    if len(timestamps) >= RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later.",
        )

    timestamps.append(now)
    request_log[client_ip] = timestamps

# -----------------------------------------------------------
# Pydantic models
# -----------------------------------------------------------
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
    reply: str

# -----------------------------------------------------------
# Health / root
# -----------------------------------------------------------
@app.get("/")
async def read_root():
    return {"status": "ok", "message": "Chatbot API running"}

# -----------------------------------------------------------
# Main chat endpoint
# -----------------------------------------------------------
@app.post(
    "/chat",
    response_model=ChatResponse,
    dependencies=[Depends(verify_api_key), Depends(rate_limiter)],
)
async def chat_endpoint(payload: ChatRequest, request: Request):
    reply_text = generate_reply(payload.message, payload.history or [])
    return ChatResponse(reply=reply_text)
