# agents.py

class Agent:
    def __init__(self, name):
        self.name = name

class Runner:
    def __init__(self, agent):
        self.agent = agent

class AsyncOpenAI:
    def chat(self, prompt):
        return f"Mock response to: {prompt}"

class OpenAIChatCompletionsModel:
    pass

class RunConfig:
    pass

