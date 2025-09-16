import ollama
import numpy as np


EMB_DIM = 768

emb_model = "hf.co/CompendiumLabs/bge-base-en-v1.5-gguf:Q4_K_M"


def embed_text(text: str) -> np.ndarray:
    res = ollama.embeddings(model=emb_model, prompt=text)
    return np.asarray(res["embedding"], dtype=np.float32)
