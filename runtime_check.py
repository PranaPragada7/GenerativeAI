"""Check real runtime APIs without downloading models or calling providers."""


def main() -> None:
    from google import genai
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_ollama import ChatOllama
    from pypdf import PdfReader
    from transformers.pipelines import check_task

    for task in ("summarization", "text-classification", "zero-shot-classification"):
        check_task(task)
    assert all((genai.Client, ChatGoogleGenerativeAI, ChatOllama, PdfReader))
    print("Runtime imports and pipeline tasks are available.")


if __name__ == "__main__":
    main()
