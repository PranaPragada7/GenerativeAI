"""Demonstrate common Gemini generation parameters through LangChain."""

import os


def generate_haiku(temperature: float = 0.8, max_tokens: int = 100) -> str:
    """Generate a short poem with configurable sampling parameters."""
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set GEMINI_API_KEY or GOOGLE_API_KEY before running this example."
        )

    from langchain_core.messages import HumanMessage
    from langchain_google_genai import ChatGoogleGenerativeAI

    model = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        google_api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    response = model.invoke([HumanMessage(content="Generate a haiku about the ocean.")])
    return str(response.content)


def main() -> None:
    print(generate_haiku())


if __name__ == "__main__":
    main()
