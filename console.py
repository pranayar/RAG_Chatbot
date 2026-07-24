from rag import RAG

print("Loading Phone Shop AI...\n")

bot = RAG()

print("Phone Shop AI is ready!")
print("Type 'exit' to quit.\n")

while True:

    question = input("You: ").strip()

    if question.lower() in ["exit", "quit"]:
        break

    print("\nAssistant: ", end="", flush=True)

    answer, sources = bot.chat(
        question,
        callback=lambda token: print(token, end="", flush=True)
    )

    print("\n")

    if sources:
        print("Sources:")
        for s in sources:
            print(" •", s)

    print()