import time
import os

class LLMClient:
    def __init__(self, provider="openai", api_key=None):
        self.provider = provider
        self.api_key = api_key
        
        if self.provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        elif self.provider == "gemini":
            from google import genai
            self.client = genai.Client(api_key=api_key)

    def query(self, system_prompt, user_prompt, model=None):
        max_retries = 3
        retry_delay = 10  # Start with 10 seconds for Gemini 429s

        for attempt in range(max_retries + 1):
            try:
                if self.provider == "openai":
                    model = model or "gpt-4o"
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ]
                    )
                    return response.choices[0].message.content
                
                elif self.provider == "gemini":
                    # The new SDK uses client.models.generate_content
                    # There isn't a strict "system" role in the same way as OpenAI in the simplest call,
                    # but we can use the config or just prepend. 
                    # For simplicity and robustness with the new SDK:
                    
                    model = model or "gemini-2.5-flash-lite"
                    response = self.client.models.generate_content(
                        model=model,
                        contents=f"System Instruction: {system_prompt}\n\nUser Message: {user_prompt}"
                    )
                    return response.text
                    
            except Exception as e:
                error_str = str(e)
                # Check for rate limit errors (429)
                if ("429" in error_str or "RESOURCE_EXHAUSTED" in error_str) and attempt < max_retries:
                    print(f"Rate limit hit ({self.provider}). Retrying in {retry_delay}s... (Attempt {attempt+1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print(f"Error querying LLM ({self.provider}): {e}")
                    return None
