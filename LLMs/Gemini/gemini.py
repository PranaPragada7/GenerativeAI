"""Call Gemini through LangChain's chat-model interface."""

import os


def ask(question: str, model: str | None = None) -> str:
    """Return Gemini's answer to one question."""
    from dotenv import load_dotenv
    from langchain_core.messages import HumanMessage
    from langchain_google_genai import ChatGoogleGenerativeAI

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set GEMINI_API_KEY or GOOGLE_API_KEY before running this example."
        )

    chat_model = ChatGoogleGenerativeAI(
        model=model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        google_api_key=api_key,
    )
    response = chat_model.invoke([HumanMessage(content=question)])
    return str(response.content)


def main() -> None:
    print(ask("What is the capital of Spain?"))


if __name__ == "__main__":
    main()
