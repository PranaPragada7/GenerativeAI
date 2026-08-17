"""Load a repository-local UTF-8 text document."""

from pathlib import Path

DEFAULT_TEXT = Path(__file__).resolve().parents[1] / "docs" / "sample_notes.txt"


def load_text(path: Path = DEFAULT_TEXT) -> str:
    """Return the complete contents of a UTF-8 text file."""
    return path.read_text(encoding="utf-8")


def main() -> None:
    text = load_text()
    print("Document count: 1")
    print(text[:80].strip())
    print("-" * 50)


if __name__ == "__main__":
    main()
