from agent.client import AgentClient


def execute(prompt: str) -> str:
    client = AgentClient()
    result = client.run(prompt)
    return result
