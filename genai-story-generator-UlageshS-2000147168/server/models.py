from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class UserPreferences(BaseModel):
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=3, le=120)
    language: str = Field(default="en", description="BCP-47 tag e.g., en, hi, ta, fr")
    genre: str = Field(default="adventure")
    tone: str = Field(default="whimsical")
    setting: str = Field(default="fantasy forest")
    characters: List[str] = Field(default_factory=list)
    moral_theme: str = Field(default="kindness and courage")
    reading_level: str = Field(default="child", description="child|teen|adult (content will be kept safe)")
    target_length_words: int = Field(default=800, ge=200, le=2000)
    constraints: Optional[str] = Field(default=None, description="Extra constraints: e.g., 'no scary scenes'")

    @field_validator("language")
    def validate_language(cls, v):
        return v.strip().lower()

class StoryRequest(BaseModel):
    preferences: UserPreferences
    seed: Optional[int] = Field(default=None)
    temperature: Optional[float] = Field(default=None)
    max_tokens: Optional[int] = Field(default=None)

class StoryJSON(BaseModel):
    title: str
    outline: List[str]
    story: str
    language: str
    words: int
    reading_level: str
    moral: str

class HealthStatus(BaseModel):
    status: str
    provider: str
    model: str
