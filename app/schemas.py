from typing import List, Literal, Optional
from pydantic import BaseModel

class Message(BaseModel):
    role: Literal["system","user","assistant"]
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.2
    max_tokens: Optional[int] = 256

class ChatChoice(BaseModel):
    index: int
    message: Message
    finish_reason: str = "stop"

class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    choices: List[ChatChoice]
    model: str

class EmbedRequest(BaseModel):
    model: str
    input: List[str]

class EmbedData(BaseModel):
    index: int
    embedding: List[float]

class EmbedResponse(BaseModel):
    object: str = "list"
    data: List[EmbedData]
    model: str
