# Hugging Face backend (CPU baseline)
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
import torch
from typing import List

class HFChat:
    def __init__(self, model_id: str = "distilgpt2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id)
        self.model.eval()

    def chat(self, messages: List[dict], max_new_tokens: int = 128, temperature: float = 0.2) -> str:
        text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            out = self.model.generate(**inputs, do_sample=temperature>0.0, max_new_tokens=max_new_tokens)
        return self.tokenizer.decode(out[0], skip_special_tokens=True)

class HFEmbed:
    def __init__(self, model_id: str = "sentence-transformers/all-MiniLM-L6-v2"):
        from transformers import AutoTokenizer, AutoModel
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModel.from_pretrained(model_id)
        self.model.eval()

    def embed(self, texts: List[str]) -> List[List[float]]:
        import torch
        with torch.no_grad():
            inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
            outputs = self.model(**inputs)
            # mean pooling
            last_hidden = outputs.last_hidden_state
            mask = inputs.attention_mask.unsqueeze(-1).expand(last_hidden.size()).float()
            embeddings = (last_hidden * mask).sum(1) / mask.sum(1)
            return embeddings.cpu().tolist()
