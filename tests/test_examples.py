"""Offline checks for example portability and import safety."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = [
    ROOT / "environment_check.py",
    ROOT / "LLMs" / "Gemini" / "gemini.py",
    ROOT / "LLMs" / "Gemini" / "gemini_2.py",
    ROOT / "LLMs" / "Gemini" / "parameters.py",
    ROOT / "LLMs" / "Huggingface_Hub" / "hf_hub_textclassification.py",
    ROOT / "LLMs" / "Huggingface_Hub" / "hf_hub_zeroshot.py",
    ROOT / "LLMs" / "Ollama" / "llm_chat.py",
    ROOT / "LLMs" / "Pipelines" / "text_summarise.py",
    ROOT / "Rag" / "Loaders" / "pdf_loader.py",
    ROOT / "Rag" / "Loaders" / "text_loader.py",
    ROOT / "Rag" / "docs" / "textloader_demo.py",
]


def import_from_path(path: Path):
    module_name = "example_" + "_".join(path.relative_to(ROOT).parts).replace(".", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda path: path.stem)
def test_examples_import_without_side_effects(path: Path):
    module = import_from_path(path)
    assert callable(module.main)


def test_loader_defaults_use_repository_documents():
    pdf_loader = import_from_path(ROOT / "Rag" / "Loaders" / "pdf_loader.py")
    text_loader = import_from_path(ROOT / "Rag" / "Loaders" / "text_loader.py")

    assert pdf_loader.DEFAULT_PDF == ROOT / "Rag" / "docs" / "generative_ai_course.pdf"
    assert text_loader.DEFAULT_TEXT == ROOT / "Rag" / "docs" / "sample_notes.txt"
    assert pdf_loader.DEFAULT_PDF.is_file()
    assert text_loader.DEFAULT_TEXT.is_file()

    pages = pdf_loader.load_pdf()
    text = text_loader.load_text()
    assert len(pages) == 1
    assert "Practical Generative AI" in pages[0]
    assert "Grades" not in pages[0]
    assert "Generative AI systems produce new content" in text

    removed_samples = {
        "courses_offered.pdf",
        "demo_pdf.pdf",
        "mlk.txt",
        "offline_faqs.txt",
        "online_faqs.txt",
    }
    assert not removed_samples.intersection(
        path.name for path in (ROOT / "Rag" / "docs").iterdir()
    )


def test_source_has_no_machine_specific_paths():
    searchable = [*EXAMPLES, Path(__file__), ROOT / "README.md"]
    placeholder = "<" + "repo-url" + ">"
    for path in searchable:
        text = path.read_text(encoding="utf-8")
        assert "C:\\Users\\" not in text
        assert placeholder not in text
