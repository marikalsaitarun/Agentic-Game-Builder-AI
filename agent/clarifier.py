from agent.llm_client import LLMClient
import os

class Clarifier:
    def __init__(self, api_key, provider="openai"):
        self.llm = LLMClient(provider, api_key)
        with open(os.path.join("prompts", "clarification_system.txt"), "r") as f:
            self.system_prompt = f.read()

    def clarify_requirements(self, initial_prompt):
        conversation_history = f"User Initial Idea: {initial_prompt}\n"
        
        while True:
            # Ask the LLM if it needs more info or if it has enough to build the game
            llm_response = self.llm.query(self.system_prompt, conversation_history)
            
            if not llm_response:
                return None
            
            print(f"\nAI: {llm_response}")
            
            if "FINAL_REQUIREMENTS:" in llm_response:
                # Extract the requirements part
                return llm_response.split("FINAL_REQUIREMENTS:")[1].strip()
            
            # Get user answer
            user_input = input("You: ")
            conversation_history += f"AI Question: {llm_response}\nUser Answer: {user_input}\n"
