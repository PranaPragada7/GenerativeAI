"""Minimal text-loader example kept beside its sample document."""

from pathlib import Path

DOCUMENT = Path(__file__).resolve().with_name("sample_notes.txt")


def main() -> None:
    text = DOCUMENT.read_text(encoding="utf-8")
    print("Document count: 1")
    print(f"Size: {len(text)}")
    print(text[:80].strip())
    print("-" * 50)


if __name__ == "__main__":
    main()
