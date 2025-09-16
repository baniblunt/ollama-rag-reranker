from src.rag.llm import generate_answer
from src.db.db_handler import TextDB


def main():
    db = TextDB()
    db.add_data("data/cat-facts.txt")

    query_1 = "How much time does a cat sleep?"
    query_2 = "What birds and cat have in common?"
    ctx_texts = db.search_texts(query_1, k=40)
    ranked_texts = db.rerank_texts(query_1, ctx_texts, k=44)
    context = "\n\n".join(ranked_texts)
    response = generate_answer(query=query_1, context=context)
    print(f"Query 1: {query_1}")
    print(f"Context: {context}")
    print(f"Response: {response}")
    ctx_texts = db.search_texts(query_2, k=40)
    ranked_texts = db.rerank_texts(query_2, ctx_texts, k=4)
    context = "\n\n".join(ranked_texts)
    response = generate_answer(query=query_2, context=context)
    print("\n\n")
    print(f"Query 2: {query_2}")
    print(f"Context: {context}")
    print(f"Response: {response}")


if __name__ == "__main__":
    main()
