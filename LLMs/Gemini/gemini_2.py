"""Call Gemini directly with the Google Gen AI SDK."""

import os

DEFAULT_PROMPT = "List five of the world's largest cities by population."


def generate(prompt: str = DEFAULT_PROMPT, model: str | None = None) -> str:
    """Generate a response with an explicitly configured API key."""
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set GEMINI_API_KEY or GOOGLE_API_KEY before running this example."
        )

    from google import genai

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt,
    )
    return response.text or ""


def main() -> None:
    print(generate())


if __name__ == "__main__":
    main()
