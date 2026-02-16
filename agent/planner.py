from agent.llm_client import LLMClient
import os

class Planner:
    def __init__(self, api_key, provider="openai"):
        self.llm = LLMClient(provider, api_key)
        with open(os.path.join("prompts", "planning_system.txt"), "r") as f:
            self.system_prompt = f.read()

    def create_plan(self, requirements):
        user_prompt = f"Create a Game Design Document for the following requirements:\n{requirements}"
        plan = self.llm.query(self.system_prompt, user_prompt)
        return plan
