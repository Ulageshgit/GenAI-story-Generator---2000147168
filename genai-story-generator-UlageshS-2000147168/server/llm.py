import os
from typing import Optional

# Providers
USE_PROVIDER = os.getenv("LLM_PROVIDER", "openai").strip().lower()

class BaseLLM:
    def __init__(self, temperature: float = 0.8, max_tokens: int = 1200):
        self.temperature = temperature
        self.max_tokens = max_tokens

    def name(self) -> str:
        raise NotImplementedError

    def generate_json(self, system: str, user: str) -> str:
        raise NotImplementedError

class AzureOpenAIProvider(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("temperature", 0.8), kwargs.get("max_tokens", 1200))
        from azure.ai.openai import OpenAI
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        if not endpoint or not api_key:
            raise RuntimeError("Missing AZURE_OPENAI_ENDPOINT/AZURE_OPENAI_API_KEY in .env")
        self.client = OpenAI(endpoint=endpoint, api_key=api_key)
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")

    def name(self) -> str:
        return f"azure:{self.deployment}"

    def generate_json(self, system: str, user: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format={"type": "json_object"},
        )
        return completion.choices[0].message.content

class OpenAIProvider(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("temperature", 0.8), kwargs.get("max_tokens", 1200))
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Missing OPENAI_API_KEY in .env")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def name(self) -> str:
        return f"openai:{self.model}"

    def generate_json(self, system: str, user: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format={"type": "json_object"},
        )
        return completion.choices[0].message.content


def make_llm(temperature: Optional[float], max_tokens: Optional[int]) -> BaseLLM:
    temp = float(temperature or float(os.getenv("DEFAULT_TEMPERATURE", "0.8")))
    mtok = int(max_tokens or int(os.getenv("DEFAULT_MAX_TOKENS", "1200")))
    if USE_PROVIDER == "azure":
        return AzureOpenAIProvider(temperature=temp, max_tokens=mtok)
    return OpenAIProvider(temperature=temp, max_tokens=mtok)
