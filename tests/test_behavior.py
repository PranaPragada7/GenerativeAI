"""Behavioral tests that keep provider examples offline and deterministic."""

import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest
from test_examples import ROOT, import_from_path


def module(path: str):
    """Import an example from a repository-relative path."""
    return import_from_path(ROOT / Path(path))


@pytest.fixture
def fake_dotenv(monkeypatch):
    dotenv = ModuleType("dotenv")
    dotenv.load_dotenv = lambda: None
    monkeypatch.setitem(sys.modules, "dotenv", dotenv)


def install_langchain_messages(monkeypatch):
    messages = ModuleType("langchain_core.messages")
    messages.HumanMessage = lambda content: SimpleNamespace(content=content)
    core = ModuleType("langchain_core")
    core.messages = messages
    monkeypatch.setitem(sys.modules, "langchain_core", core)
    monkeypatch.setitem(sys.modules, "langchain_core.messages", messages)


def test_direct_gemini_uses_configured_key_and_model(monkeypatch, fake_dotenv):
    calls = {}

    class Client:
        def __init__(self, api_key):
            calls["api_key"] = api_key
            self.models = self

        def generate_content(self, **kwargs):
            calls.update(kwargs)
            return SimpleNamespace(text="Madrid")

    genai = ModuleType("google.genai")
    genai.Client = Client
    google = ModuleType("google")
    google.genai = genai
    monkeypatch.setitem(sys.modules, "google", google)
    monkeypatch.setitem(sys.modules, "google.genai", genai)
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    example = module("LLMs/Gemini/gemini_2.py")

    assert example.generate("Capital?", model="test-model") == "Madrid"
    assert calls == {
        "api_key": "test-key",
        "model": "test-model",
        "contents": "Capital?",
    }


def test_direct_gemini_requires_credentials(monkeypatch, fake_dotenv):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    example = module("LLMs/Gemini/gemini_2.py")

    with pytest.raises(RuntimeError, match="GEMINI_API_KEY"):
        example.generate("Hello")


def test_langchain_gemini_returns_message_content(monkeypatch, fake_dotenv):
    calls = {}
    install_langchain_messages(monkeypatch)

    class ChatModel:
        def __init__(self, **kwargs):
            calls.update(kwargs)

        def invoke(self, messages):
            calls["prompt"] = messages[0].content
            return SimpleNamespace(content="Madrid")

    provider = ModuleType("langchain_google_genai")
    provider.ChatGoogleGenerativeAI = ChatModel
    monkeypatch.setitem(sys.modules, "langchain_google_genai", provider)
    monkeypatch.setenv("GOOGLE_API_KEY", "google-key")

    example = module("LLMs/Gemini/gemini.py")

    assert example.ask("Capital?", model="test-model") == "Madrid"
    assert calls["model"] == "test-model"
    assert calls["google_api_key"] == "google-key"
    assert calls["prompt"] == "Capital?"


def test_generation_parameters_are_forwarded(monkeypatch, fake_dotenv):
    calls = {}
    install_langchain_messages(monkeypatch)

    class ChatModel:
        def __init__(self, **kwargs):
            calls.update(kwargs)

        def invoke(self, messages):
            calls["prompt"] = messages[0].content
            return SimpleNamespace(content="Blue tide\nMoonlit and quiet\nDawn")

    provider = ModuleType("langchain_google_genai")
    provider.ChatGoogleGenerativeAI = ChatModel
    monkeypatch.setitem(sys.modules, "langchain_google_genai", provider)
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    example = module("LLMs/Gemini/parameters.py")

    result = example.generate_haiku(temperature=0.3, max_tokens=40)
    assert "Blue tide" in result
    assert calls["temperature"] == 0.3
    assert calls["max_tokens"] == 40
    assert "haiku" in calls["prompt"]


def test_ollama_uses_model_override(monkeypatch, fake_dotenv):
    calls = {}

    class ChatModel:
        def __init__(self, **kwargs):
            calls.update(kwargs)

        def invoke(self, prompt):
            calls["prompt"] = prompt
            return SimpleNamespace(content="Canberra")

    provider = ModuleType("langchain_ollama")
    provider.ChatOllama = ChatModel
    monkeypatch.setitem(sys.modules, "langchain_ollama", provider)
    monkeypatch.setenv("OLLAMA_MODEL", "local-model")

    example = module("LLMs/Ollama/llm_chat.py")

    assert example.ask("Capital?") == "Canberra"
    assert calls == {"model": "local-model", "prompt": "Capital?"}


@pytest.mark.parametrize(
    ("path", "task", "result"),
    [
        (
            "LLMs/Huggingface_Hub/hf_hub_textclassification.py",
            "text-classification",
            [{"label": "POSITIVE", "score": 0.99}],
        ),
        (
            "LLMs/Huggingface_Hub/hf_hub_zeroshot.py",
            "zero-shot-classification",
            {"labels": ["technology"], "scores": [0.98]},
        ),
    ],
)
def test_classification_pipelines(monkeypatch, path, task, result):
    calls = {}

    def pipeline(selected_task, **kwargs):
        calls.update(task=selected_task, **kwargs)

        def run(*args):
            calls["arguments"] = args
            return result

        return run

    transformers = ModuleType("transformers")
    transformers.pipeline = pipeline
    monkeypatch.setitem(sys.modules, "transformers", transformers)

    example = module(path)
    output = example.classify("A faster processor")

    assert output == result
    assert calls["task"] == task
    assert calls["arguments"][0] == "A faster processor"


def test_summarizer_forwards_generation_limits(monkeypatch):
    calls = {}

    def pipeline(task, **kwargs):
        calls.update(task=task, **kwargs)

        def run(text, **options):
            calls.update(text=text, options=options)
            return [{"summary_text": "A concise summary."}]

        return run

    transformers = ModuleType("transformers")
    transformers.pipeline = pipeline
    monkeypatch.setitem(sys.modules, "transformers", transformers)

    example = module("LLMs/Pipelines/text_summarise.py")

    assert example.summarize("Long article", min_length=3, max_length=12) == (
        "A concise summary."
    )
    assert calls["task"] == "summarization"
    assert calls["options"] == {
        "max_length": 12,
        "min_length": 3,
        "do_sample": False,
    }


def test_environment_check_reports_missing_package(monkeypatch, capsys):
    example = module("environment_check.py")
    monkeypatch.setattr(example, "PACKAGES", ("installed", "missing"))

    def fake_version(package):
        if package == "missing":
            raise example.PackageNotFoundError
        return "1.2.3"

    monkeypatch.setattr(example, "version", fake_version)
    example.main()

    output = capsys.readouterr().out
    assert "installed: 1.2.3" in output
    assert "missing: not installed" in output


def test_document_loader_entry_points(capsys):
    for path in (
        "Rag/Loaders/text_loader.py",
        "Rag/Loaders/pdf_loader.py",
        "Rag/docs/textloader_demo.py",
    ):
        module(path).main()

    output = capsys.readouterr().out
    assert "Document count: 1" in output
    assert "Page count: 1" in output
    assert "Practical Generative AI" in output
