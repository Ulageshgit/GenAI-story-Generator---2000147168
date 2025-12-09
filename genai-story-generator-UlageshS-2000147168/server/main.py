import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .models import StoryRequest, HealthStatus, StoryJSON
from .prompt import SYSTEM_PROMPT, user_prompt
from .llm import make_llm
from .postprocess import extract_first_json_block, safety_postprocess, ensure_fields

load_dotenv()

app = FastAPI(title="GEN AI Personalized Story Generator", version="1.0.0")

# CORS for the simple browser frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for local dev; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthStatus)
def health():
    llm = make_llm(None, None)
    return HealthStatus(status="ok", provider=llm.name(), model=llm.name())

@app.post("/generate", response_model=StoryJSON)
def generate(req: StoryRequest):
    llm = make_llm(req.temperature, req.max_tokens)
    u_prompt = user_prompt(req.preferences, seed=req.seed)
    try:
        raw = llm.generate_json(SYSTEM_PROMPT, u_prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

    parsed = extract_first_json_block(raw)
    if not parsed:
        raise HTTPException(status_code=500, detail="Model did not return valid JSON.")

    # Safety and defaults
    parsed = safety_postprocess(parsed)
    parsed = ensure_fields(parsed, {
        "language": req.preferences.language,
        "target_length_words": req.preferences.target_length_words,
        "reading_level": req.preferences.reading_level,
        "moral_theme": req.preferences.moral_theme,
    })

    # Final model to return validation via Pydantic
    return StoryJSON(**parsed)
