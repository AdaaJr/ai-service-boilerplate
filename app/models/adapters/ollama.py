# Ollama backend
import httpx
from typing import List

class OllamaChat:
    def __init__(self, host: str = "http://localhost:11434", model: str = "llama3"):
        self.host = host; self.model = model
    def chat(self, messages: List[dict], max_new_tokens: int = 128, temperature: float = 0.2) -> str:
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        r = httpx.post(f"{self.host}/api/generate", json={"model": self.model, "prompt": prompt})
        r.raise_for_status(); data = r.json()
        return data.get("response","")

class OllamaEmbed:
    def __init__(self, host: str = "http://localhost:11434", model: str = "nomic-embed-text"):
        self.host = host; self.model = model
    def embed(self, texts: List[str]) -> List[List[float]]:
        out = []
        for t in texts:
            r = httpx.post(f"{self.host}/api/embeddings", json={"model": self.model, "prompt": t})
            r.raise_for_status(); out.append(r.json().get("embedding", []))
        return out
