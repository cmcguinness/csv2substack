# Repository Guidelines

## Project Structure & Module Organization
- `main.py`: CLI tool to convert CSV into LaTeX array markup suitable for Substack.
- `README.md`: Basic usage notes. Keep in sync with CLI flags and file names.
- `goals.csv`: Sample data (ignored by Git via `.gitignore`).
- `.venv/`, `.idea/`, `__pycache__/`: Local/dev artifacts; do not commit.
- Tests (when added) should live under `tests/`.

## Build, Test, and Development Commands
- Setup (Python 3.9+):
  - `python3 -m venv .venv && source .venv/bin/activate`
  - `python -m pip install -U pip`
- Run help/CLI:
  - `python main.py --help`
  - Example: `python main.py data.csv --header --grid --align l -o table.tex`
  - GUI picker: `python main.py --tk`
- Tests (if present):
  - `pytest -q` (place tests in `tests/test_*.py`).

## Coding Style & Naming Conventions
- Follow PEP 8; use 4-space indentation.
- Names: `snake_case` for functions/vars, `CapWords` for classes, `ALL_CAPS` for constants.
- Prefer type hints and short docstrings describing purpose and return values.
- Keep the project stdlib-only unless a strong reason exists; update `README.md` if dependencies are introduced.
- CLI flags should be descriptive and stable; document new flags in `--help` and `README.md` with examples.

## Testing Guidelines
- Framework: `pytest` (recommended). New tests under `tests/` as `test_*.py`.
- Cover: argument parsing, preference translation, LaTeX escaping, and grid/format variations.
- Use small in-memory CSVs via `io.StringIO` to avoid filesystem writes.
- Aim for fast, deterministic tests; no network or GUI in tests.

## Commit & Pull Request Guidelines
- Commits: small, focused, imperative mood (e.g., "Add grid option to output").
- PRs include: motivation, summary of changes, before/after CLI examples, and any user-facing behavior changes.
- Link related issues; add screenshots only when GUI behavior is relevant.
- If you rename files or flags, update `README.md` and examples.

## Security & Configuration Tips
- Treat CSV as untrusted text; never execute input.
- Ensure LaTeX-special chars are escaped (see `escape_latex_chars`).
- Default to stdout; only write files when `-o/--output` is provided.
