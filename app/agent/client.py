import os
import asyncio


class AgentClient:
    def __init__(self):
        self.agent = None
        self.provider_configured = False
        self.provider = os.getenv("DEFAULT_LLM_PROVIDER", "gemini").lower()
        self.model = os.getenv("DEFAULT_MODEL", "gemini-2.5-pro")
        self.required_key_env = None
        self.init_error = None
        try:
            from spoon_ai.chat import ChatBot
            from spoon_ai.agents.toolcall import ToolCallAgent

            class BackendAgent(ToolCallAgent):
                name: str = "backend_agent"
                description: str = "Backend SpoonOS agent"
                system_prompt: str = "You are the AOL backend AI agent."

            key_map = {
                "openai": "OPENAI_API_KEY",
                "anthropic": "ANTHROPIC_API_KEY",
                "gemini": "GOOGLE_API_KEY",
                "deepseek": "DEEPSEEK_API_KEY",
                "openrouter": "OPENROUTER_API_KEY",
            }
            key_env = key_map.get(self.provider)
            # Accept both GEMINI_API_KEY and GOOGLE_API_KEY for Gemini
            if self.provider == "gemini":
                gemini_key = os.getenv("GEMINI_API_KEY")
                google_key = os.getenv("GOOGLE_API_KEY")
                api_key = gemini_key or google_key
                self.required_key_env = "GEMINI_API_KEY" if gemini_key else ("GOOGLE_API_KEY" if google_key else key_env)
            else:
                api_key = os.getenv(key_env) if key_env else None
                self.required_key_env = key_env
            self.provider_configured = bool(api_key)

            try:
                llm = ChatBot(llm_provider=self.provider, model_name=self.model)
            except Exception as e:
                self.init_error = str(e)
                llm = ChatBot(llm_provider=self.provider)
            self.agent = BackendAgent(llm=llm)
        except Exception as e:
            self.agent = None
            self.init_error = str(e)

    def is_spoon_available(self) -> bool:
        return self.agent is not None and self.provider_configured

    async def arun(self, prompt: str):
        if self.is_spoon_available():
            return await self.agent.run(prompt)
        return prompt

    def run(self, prompt: str):
        try:
            loop = asyncio.get_running_loop()
            if loop and self.is_spoon_available():
                return loop.run_until_complete(self.agent.run(prompt))
        except RuntimeError:
            pass
        if self.is_spoon_available():
            return asyncio.run(self.agent.run(prompt))
        return prompt

    def metadata(self) -> dict:
        return {
            "provider": self.provider,
            "model": self.model,
            "spoon_available": self.is_spoon_available(),
            "required_key": self.required_key_env,
            "init_error": self.init_error,
        }
