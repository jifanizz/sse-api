# sse-api

Python tooling for the Cisco SSE API.

## Requirements

Python 3.13+

## Installation

**uv** (recommended):

```bash
uv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

**pip:**

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

If project dependencies live in `pyproject.toml` with a lockfile, use `uv sync` instead of `uv pip install`.

## Usage

```bash
cd private-resource
```

Add a `.env` file next to the notebook. Values come from the SSE GUI; the notebook loads them with `dotenv`.



```env
API_KEY='from_SSE_GUI'
API_SECRET='from_SSE_GUI'
```

Do not commit `.env` or credentials.

**Notebook** — from `private-resource/`, run `main.ipynb` for a stepped process to create SSE private-resources.


## Project layout

| Path | Purpose |
|------|---------|
| `main.py` | CLI entrypoint |
| `pyproject.toml` | Project metadata |
| `requirements.txt` | Dependencies |
| `private-resource/` | Notebook and local assets |

## Development

When dependencies change, update `requirements.txt` or the lockfile and reinstall.
