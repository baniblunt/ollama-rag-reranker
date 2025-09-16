import ollama


model = "hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF:Q4_K_M"
system_prompt = "You are given a question and a context. You need to answer the question based on the context"


def generate_answer(query: str, context: str) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Question: {query}\n\nContext:\n{context}"},
    ]
    answer = ollama.chat(model=model, messages=messages)
    return answer["message"]["content"]
