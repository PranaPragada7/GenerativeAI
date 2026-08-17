"""Print the Python version and availability of optional example packages."""

from importlib.metadata import PackageNotFoundError, version
from platform import python_version

PACKAGES = (
    "google-genai",
    "langchain-core",
    "langchain-google-genai",
    "langchain-ollama",
    "transformers",
    "pypdf",
)


def installed_version(package: str) -> str:
    """Return an installed package version or a clear missing marker."""
    try:
        return version(package)
    except PackageNotFoundError:
        return "not installed"


def main() -> None:
    """Print a concise environment summary without importing heavy libraries."""
    print(f"Python: {python_version()}")
    for package in PACKAGES:
        print(f"{package}: {installed_version(package)}")


if __name__ == "__main__":
    main()
