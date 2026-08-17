"""Send a chat prompt to a locally running Ollama model."""

import os


def ask(question: str) -> str:
    """Return the content produced by the configured local model."""
    from dotenv import load_dotenv
    from langchain_ollama import ChatOllama

    load_dotenv()
    model = ChatOllama(model=os.getenv("OLLAMA_MODEL", "llama3.2"))
    return str(model.invoke(question).content)


def main() -> None:
    print(ask("What is the capital of Australia?"))


if __name__ == "__main__":
    main()
