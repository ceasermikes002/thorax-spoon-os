from typing import Optional


class AgentClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def run(self, prompt: str) -> str:
        try:
            import spoon_ai  # noqa: F401
        except Exception:
            return prompt
        return prompt

