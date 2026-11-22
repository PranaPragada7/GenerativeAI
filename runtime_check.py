"""Check real runtime APIs without downloading models or calling providers."""


def main() -> None:
    from google import genai
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_ollama import ChatOllama
    from pypdf import PdfReader
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    from transformers.pipelines import check_task

    for task in ("text-classification", "zero-shot-classification"):
        check_task(task)
    assert all(
        (
            genai.Client,
            ChatGoogleGenerativeAI,
            ChatOllama,
            PdfReader,
            AutoModelForSeq2SeqLM.from_pretrained,
            AutoTokenizer.from_pretrained,
        )
    )
    print("Runtime imports and pipeline tasks are available.")


if __name__ == "__main__":
    main()
