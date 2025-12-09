SYSTEM_PROMPT = """You are a helpful, creative story author that writes safe, engaging stories for a general audience.
Hard safety requirements:
- Do not include sexual, pornographic, erotic, violent gore, or age-inappropriate content.
- Avoid hateful, harassing, or dangerous content.
- Keep content suitable for a general audience, including children when reading_level=child.

Output strictly as JSON **only**, following this schema:
{
  "title": string,
  "outline": string[],   // 5-10 bullet points
  "story": string,       // 500-1500 words depending on target_length_words
  "language": string,    // BCP-47 tag
  "words": number,       // approximate word count
  "reading_level": string, // child|teen|adult
  "moral": string
}
Do NOT include markdown fences or commentary—return JSON only.
"""

def user_prompt(preferences, seed=None):
    chars = preferences.characters or []
    chars_str = ", ".join(chars) if chars else "original supporting characters as needed"

    extras = f"
Extra constraints: {preferences.constraints}" if preferences.constraints else ""

    return f"""Write a personalized story with these inputs:
Name: {preferences.name}
Age: {preferences.age}
Language: {preferences.language}
Genre: {preferences.genre}
Tone: {preferences.tone}
Setting: {preferences.setting}
Characters: {chars_str}
Moral Theme: {preferences.moral_theme}
Reading Level: {preferences.reading_level}
Target Length (words): {preferences.target_length_words}{extras}

Personalization guidelines:
- Use the name naturally (avoid overuse).
- Reflect age and reading_level in vocabulary and sentence complexity.
- Align genre and tone throughout; avoid sudden style shifts.
- Keep scenes safe, uplifting, and suitable for general audiences.
- If language is not English, write fully in that language.
- Include a clear moral aligned to moral_theme.
- Keep narrative coherent with an outline, then craft a continuous story.

Seed (for reproducibility): {seed if seed is not None else "none"}
"""
