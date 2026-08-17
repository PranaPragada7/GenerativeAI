"""Run a local sentiment-classification pipeline."""


def classify(text: str) -> list[dict]:
    """Classify sentiment with a small, public Hugging Face model."""
    from transformers import pipeline

    classifier = pipeline(
        "text-classification",
        model="distilbert-base-uncased-finetuned-sst-2-english",
    )
    return classifier(text)


def main() -> None:
    print(classify("I love this movie!"))


if __name__ == "__main__":
    main()
