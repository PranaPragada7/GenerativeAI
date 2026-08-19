# Contributing

Contributions should keep each example small, independent, and safe to import.

1. Create a branch from `main`.
2. Keep credentials in environment variables and update `.env.example` when needed.
3. Avoid network calls, model downloads, or console output during module import.
4. Add offline tests for new behavior.
5. Run the validation commands in the README before opening a pull request.

Examples should use repository-relative paths and include a clear error when an
optional service or local model is unavailable.
