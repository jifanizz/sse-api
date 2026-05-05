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

**.env**

Add a `.env` file next to the notebook. Values come from the SSE GUI; the notebook loads them with `dotenv`.



```env
API_KEY='from_SSE_GUI'
API_SECRET='from_SSE_GUI'
```

Do not commit `.env` or credentials.


If project dependencies live in `pyproject.toml` with a lockfile, use `uv sync` instead of `uv pip install`.

## Private Resource API Creation on SSE

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

## Access-Policy API Creation on SSE

```bash
cd access-policy
```


**Notebook** — from `access-policy/`, run `main.ipynb` for a stepped process to create SSE Access-Policy Rules.



When dependencies change, update `requirements.txt` or the lockfile and reinstall.
