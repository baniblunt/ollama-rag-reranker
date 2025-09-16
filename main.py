from src.db.db_handler import TextDB
from src.rag.llm import generate_answer

CYAN = "\033[36m"
YELLOW = "\033[33m"
GRAY = "\033[90m"
RESET = "\033[0m"


def print_menu(k: int, mode: str) -> None:
    title = f" RAG MENU | k={k} | mode={mode} "
    width = len(title)
    if width < 40:
        width = 80
    bar = "=" * width
    print(f"\n{CYAN}{bar}{RESET}")
    print(f"{CYAN}{title:^{width}}{RESET}")
    print(f"{CYAN}{bar}{RESET}")
    print("  1) Ask question")
    print(f"  2) Change k {GRAY}(current: {k}){RESET}")
    print(f"  3) Change mode {GRAY}(current: {mode}){RESET}  [none | rerank | both]")
    print("  4) Exit")
    print(f"{CYAN}{bar}{RESET}")


def show(tag: str, q: str, texts: list[str], k: int) -> None:
    chosen = texts[:k]
    print(f"\n{YELLOW}--- {tag} ANSWER ---{RESET}")
    ans = generate_answer(query=q, context="\n\n".join(chosen))
    print(ans)
    print(f"\n{YELLOW}--- {tag} CONTEXT ---{RESET}")
    for i, t in enumerate(chosen, start=1):
        print(f"{GRAY}[{i}] {t}{RESET}")


# "How much time does a cat sleep?"
# "What birds and cat have in common?"


def main():
    db = TextDB()
    db.add_data("data/cat-facts.txt")

    k = 6
    mode = "none"  # none | rerank | both

    while True:
        print_menu(k, mode)
        choice = input("Select: ").strip()
        match choice:
            case "1":
                q = input("Question: ").strip()
                if not q:
                    continue

                candidates = db.search_texts(q, k=40)

                if mode in {"none", "both"}:
                    show("NO-RERANK", q, candidates, k)
                if mode in {"rerank", "both"}:
                    reranked = db.rerank_texts(q, candidates, k=k)
                    show("RERANK", q, reranked, k)
            case "2":

                k = max(1, int(input("New k: ").strip()))

            case "3":
                m = input("Mode [none|rerank|both]: ").strip().lower()
                if m in {"none", "rerank", "both"}:
                    mode = m
                else:
                    print("Invalid mode")
            case "4" | "0" | "q" | "Q":
                print("Bye!")
                break
            case _:
                print("Choose 1-4")


if __name__ == "__main__":
    main()
