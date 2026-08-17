"""Load text from a repository-local PDF."""

from pathlib import Path

DEFAULT_PDF = Path(__file__).resolve().parents[1] / "docs" / "generative_ai_course.pdf"


def load_pdf(path: Path = DEFAULT_PDF) -> list[str]:
    """Return extracted text for each page in a PDF."""
    from pypdf import PdfReader

    return [(page.extract_text() or "") for page in PdfReader(path).pages]


def main() -> None:
    pages = load_pdf()
    print(f"Page count: {len(pages)}")
    for page in pages:
        print(page[:80].strip())
        print("-" * 50)


if __name__ == "__main__":
    main()
