"""Run zero-shot topic classification with a local pipeline."""

DEFAULT_LABELS = ["sports", "politics", "technology"]


def classify(text: str, labels: list[str] | None = None) -> dict:
    """Rank candidate labels for the supplied text."""
    from transformers import pipeline

    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    return classifier(text, labels or DEFAULT_LABELS)


def main() -> None:
    text = "The new smartphone has a faster processor and an improved camera."
    print(classify(text))


if __name__ == "__main__":
    main()
