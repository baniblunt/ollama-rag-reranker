from docarray import BaseDoc
from docarray.typing import NdArray
from vectordb import HNSWVectorDB

from src.rag.embedding import EMB_DIM, embed_text
from src.data.dataio import read_data


class TextDoc(BaseDoc):
    id: str | None = None
    text: str
    embedding: NdArray[EMB_DIM]


class TextDB:
    def __init__(self, workspace: str = "./vectordb"):
        self.db = HNSWVectorDB[TextDoc](workspace=workspace)

    def add_text(self, text: str):
        vec = embed_text(text)
        self.db.index(TextDoc(id=text, text=text, embedding=vec))

    def add_data(self, file_path: str):
        data = read_data(file_path)
        for idx, text in enumerate(data.splitlines()):
            if not text.strip():
                continue
            vec = embed_text(text)
            self.db.index(TextDoc(id=f"{file_path}:{idx}", text=text, embedding=vec))

    def search(self, query: str, k: int = 5):
        vec = embed_text(query)
        return self.db.search(TextDoc(text=query, embedding=vec), limit=k)

    def search_texts(self, query: str, k: int = 5) -> list[str]:
        res = self.search(query, k=k)
        candidate = res[0] if isinstance(res, (list, tuple)) and res else res
        matches = getattr(candidate, "matches", [])
        return [m.text for m in matches][:k]
