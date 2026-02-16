from agent.llm_client import LLMClient
import os
import re

class Executor:
    def __init__(self, api_key, provider="openai"):
        self.llm = LLMClient(provider, api_key)
        with open(os.path.join("prompts", "coding_system.txt"), "r") as f:
            self.system_prompt = f.read()

    def generate_code(self, requirements, plan):
        user_prompt = f"Generate the game code based on these requirements and plan.\nRequirements: {requirements}\nPlan: {plan}"
        response = self.llm.query(self.system_prompt, user_prompt)
        
        if not response:
            return {}

        files = {}
        # improved regex to capture filename and content
        pattern = r"### FILENAME: ([\w\.]+)\s+```(?:html|css|javascript|js)?\n(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)
        
        for filename, content in matches:
            files[filename] = content.strip()
            
        return files
