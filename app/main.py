from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import time, uuid, json, os

from app.config import settings
from app.schemas import ChatRequest, ChatResponse, ChatChoice, Message, EmbedRequest, EmbedResponse, EmbedData

app = FastAPI(title="AI Service Boilerplate 2025", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_api_key(authorization: Optional[str]):
    if settings.api_keys:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing Bearer token")
        token = authorization.split(" ", 1)[1]
        if token not in settings.api_keys:
            raise HTTPException(status_code=403, detail="Invalid API key")

def choose_backend(model: str):
    if model.startswith("hf:") or settings.model_backend == "hf":
        from app.models.adapters.hf import HFChat, HFEmbed
        chat = HFChat(model_id=(model.split("hf:")[1] if model.startswith("hf:") else settings.hf_model_id))
        embed = HFEmbed()  # separate embedding model
        return chat, embed
    if model.startswith("ollama:") or settings.model_backend == "ollama":
        from app.models.adapters.ollama import OllamaChat, OllamaEmbed
        chat = OllamaChat(model=(model.split("ollama:")[1] if model.startswith("ollama:") else "llama3"), host=settings.ollama_host)
        embed = OllamaEmbed(host=settings.ollama_host)
        return chat, embed
    # mock fallback
    class MockChat:
        def chat(self, messages, max_new_tokens=128, temperature=0.2): return "Mock response"
    class MockEmbed:
        def embed(self, texts): return [[0.0]*8 for _ in texts]
    return MockChat(), MockEmbed()

@app.get("/healthz")
def healthz():
    return {"status": "ok", "time": time.time()}

@app.post("/v1/chat/completions", response_model=ChatResponse)
def chat(req: ChatRequest, authorization: Optional[str] = Header(None)):
    check_api_key(authorization)
    chat_backend, _ = choose_backend(req.model)
    result = chat_backend.chat([m.model_dump() for m in req.messages], req.max_tokens or 128, req.temperature or 0.2)
    msg = Message(role="assistant", content=result)
    return ChatResponse(id=str(uuid.uuid4()), choices=[ChatChoice(index=0, message=msg)], model=req.model)

@app.post("/v1/embeddings", response_model=EmbedResponse)
def embeddings(req: EmbedRequest, authorization: Optional[str] = Header(None)):
    check_api_key(authorization)
    _, embed_backend = choose_backend(req.model)
    embs = embed_backend.embed(req.input)
    return EmbedResponse(data=[EmbedData(index=i, embedding=v) for i, v in enumerate(embs)], model=req.model)
