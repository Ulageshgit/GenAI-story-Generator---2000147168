import re

# Minimal heuristic safety filter; for production use Azure Content Safety.
BANNED_PATTERNS = [
    r"sex", r"sexual", r"erotic", r"porn",
    r"nsfw", r"explicit", r"violence", r"gore",
    r"rape", r"pornographic", r"fetish",
]

def is_unsafe_text(text: str) -> bool:
    if not text:
        return False
    lower = text.lower()
    return any(re.search(p, lower) for p in BANNED_PATTERNS)

def sanitize_text(text: str) -> str:
    # Light touch: if flagged, replace questionable terms.
    sanitized = text
    for p in BANNED_PATTERNS:
        sanitized = re.sub(p, "[redacted]", sanitized, flags=re.IGNORECASE)
    return sanitized
