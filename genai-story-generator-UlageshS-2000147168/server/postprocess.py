import json
import re
from typing import Optional
from .safety import is_unsafe_text, sanitize_text

def extract_first_json_block(text: str) -> Optional[dict]:
    """
    Extracts the first top-level JSON object from text.
    """
    if not text:
        return None
    # Find braces region heuristically
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    candidate = text[start:end+1]
    # Remove trailing commas issues and fix common JSON mistakes
    cleaned = re.sub(r",\s*}", "}", candidate)
    cleaned = re.sub(r",\s*]", "]", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Attempt to find a more precise block via regex
        match = re.search(r"\{(?:[^{}]|(?R))*\}", text, flags=re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
        return None

def safety_postprocess(story_json: dict) -> dict:
    """
    Ensure content safety; sanitize fields if necessary.
    """
    for key in ["title", "story", "moral"]:
        if key in story_json and isinstance(story_json[key], str):
            if is_unsafe_text(story_json[key]):
                story_json[key] = sanitize_text(story_json[key])
    # Outline items
    if "outline" in story_json and isinstance(story_json["outline"], list):
        story_json["outline"] = [sanitize_text(str(x)) for x in story_json["outline"]]
    return story_json

def ensure_fields(story_json: dict, defaults: dict) -> dict:
    """
    Fill missing fields with safe defaults.
    """
    story_json.setdefault("title", "A Personalized Tale")
    story_json.setdefault("outline", [])
    story_json.setdefault("story", "")
    story_json.setdefault("language", defaults.get("language", "en"))
    story_json.setdefault("words", max(300, defaults.get("target_length_words", 800)))
    story_json.setdefault("reading_level", defaults.get("reading_level", "child"))
    story_json.setdefault("moral", defaults.get("moral_theme", "Kindness matters"))
    return story_json
