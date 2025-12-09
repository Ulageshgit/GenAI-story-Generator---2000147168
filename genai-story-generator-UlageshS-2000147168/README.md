# GEN AI Personalized Story Generator

A fully working FastAPI + HTML/JS app that generates safe, personalized stories using an LLM (Azure OpenAI or OpenAI). It enforces a JSON schema, includes basic safety checks, and allows customization for language, genre, tone, and reading level.

## Features
- Personalized inputs: name, age, language (BCP-47), genre, tone, setting, characters, moral theme.
- Safe content filter and strict JSON output schema.
- Simple browser UI and REST API.
- Pluggable provider: Azure OpenAI or OpenAI.

## Prerequisites
- Python 3.10+
- Access to Azure OpenAI **or** OpenAI API keys.

## Setup

```bash
# 1) Clone or create the folder and enter it
cd genai-story-generator

# 2) Create virtual environment (optional)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scriptsctivate

# 3) Install backend dependencies
pip install -r server/requirements.txt

# 4) Configure environment
cp server/.env.example server/.env
# Edit server/.env and set your keys and model names

# 5) Run the backend
uvicorn server.main:app --reload

# Backend will start at http://127.0.0.1:8000
```

## Frontend
No build step needed; open `frontend/index.html` in a browser.  
Make sure `API_BASE` in `frontend/app.js` points to `http://127.0.0.1:8000`.

## API

### `POST /generate`
Request body:
```json
{
  "preferences": {
    "name": "Aarav",
    "age": 10,
    "language": "en",
    "genre": "adventure",
    "tone": "whimsical",
    "setting": "fantasy forest",
    "characters": ["Luna", "a friendly dragon"],
    "moral_theme": "kindness and courage",
    "reading_level": "child",
    "target_length_words": 800,
    "constraints": "no scary scenes"
  },
  "seed": 42,
  "temperature": 0.8,
  "max_tokens": 1200
}
```

Response body (example):
```json
{
  "title": "The Lantern of the Whispering Woods",
  "outline": ["...", "..."],
  "story": "...",
  "language": "en",
  "words": 812,
  "reading_level": "child",
  "moral": "Kindness shines brightest when we share it."
}
```

### `GET /health`
Returns provider and model info.

## Notes
- For production, replace heuristic `safety.py` with **Azure Content Safety** and add auth & rate limiting.
- To support streaming or multi-turn refinement, add WebSocket or Server-Sent Events and iterative prompts.
- You can localize UI labels for your preferred language.

## License
MIT
