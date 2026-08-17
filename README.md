# Generative AI Examples

[![CI](https://github.com/PranaPragada7/GenerativeAI/actions/workflows/ci.yml/badge.svg)](https://github.com/PranaPragada7/GenerativeAI/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-examples-1C3C3C)](https://python.langchain.com/)

A compact collection of runnable examples for comparing generative-AI providers,
local models, Hugging Face pipelines, and document loaders. Each script is
independent, uses environment variables for configuration, and avoids network or
model work during import.

## Included examples

| Area | Example | What it demonstrates |
|---|---|---|
| Gemini SDK | `LLMs/Gemini/gemini_2.py` | Direct generation with `google-genai` |
| LangChain + Gemini | `LLMs/Gemini/gemini.py` | Chat invocation through LangChain |
| Generation settings | `LLMs/Gemini/parameters.py` | Temperature and output-token controls |
| Hugging Face | `LLMs/Huggingface_Hub/` | Sentiment and zero-shot classification |
| Local models | `LLMs/Ollama/llm_chat.py` | Local chat through Ollama |
| Transformers | `LLMs/Pipelines/text_summarise.py` | Text summarization pipeline |
| Document loading | `Rag/Loaders/` | Portable text and PDF loading |

The `Rag/docs/` directory contains small documents used by the loader examples.
The repository does not currently contain a complete vector-search or agent
application; it focuses on clear building blocks that can be run separately.

## Setup

Python 3.11 or newer is recommended.

```powershell
git clone https://github.com/PranaPragada7/GenerativeAI.git
cd GenerativeAI
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

For macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

Copy the environment template before running a hosted-model example:

```powershell
Copy-Item .env.example .env
```

Add only the keys needed for the provider you want to use. `.env` is ignored by
Git and must never be committed.

## Run examples

```powershell
# Confirm the local environment
python environment_check.py

# Direct Gemini SDK
python LLMs/Gemini/gemini_2.py

# LangChain with Gemini
python LLMs/Gemini/gemini.py

# Hugging Face sentiment pipeline
python LLMs/Huggingface_Hub/hf_hub_textclassification.py

# Local Ollama chat (requires Ollama and the configured model)
python LLMs/Ollama/llm_chat.py

# Portable document loaders
python Rag/Loaders/text_loader.py
python Rag/Loaders/pdf_loader.py
```

Hugging Face examples download model weights the first time they run. The Ollama
example requires an Ollama service and a locally available model. Hosted Gemini
examples require `GEMINI_API_KEY` or `GOOGLE_API_KEY`.

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `GEMINI_API_KEY` | Gemini authentication | None |
| `GOOGLE_API_KEY` | Alternative Gemini key name | None |
| `GEMINI_MODEL` | Gemini model used by the examples | `gemini-2.5-flash` |
| `OLLAMA_MODEL` | Local Ollama model | `llama3.2` |

## Quality checks

The automated checks do not call hosted APIs or download model weights.

```powershell
python -m pip install -r requirements-dev.txt
python -m black --check .
python -m ruff check .
python -m compileall -q .
python -m pytest -q
```

## Repository structure

```text
LLMs/                 Provider and pipeline examples
Rag/Loaders/          Text and PDF loader examples
Rag/docs/             Local documents used by loaders
tests/                Offline portability and import checks
.github/workflows/    Automated quality checks
environment_check.py  Installed-package summary
```
