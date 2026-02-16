import os
import sys
from dotenv import load_dotenv
from agent.clarifier import Clarifier
from agent.planner import Planner
from agent.executor import Executor
from agent.utils import setup_logging, save_file
import colorama
from colorama import Fore, Style

# Load environment variables
load_dotenv()

def main():
    colorama.init()
    setup_logging()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    provider = "openai"
    api_key = openai_key
    
    if gemini_key:
        provider = "gemini"
        api_key = gemini_key
        print(f"{Fore.GREEN}Using Gemini API{Style.RESET_ALL}")
    elif openai_key:
        print(f"{Fore.GREEN}Using OpenAI API{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Error: Neither OPENAI_API_KEY nor GEMINI_API_KEY found.{Style.RESET_ALL}")
        print("Please set one in .env or pass it as an environment variable.")
        sys.exit(1)

    print(f"{Fore.CYAN}=== Agentic Game-Builder AI ==={Style.RESET_ALL}")
    print("I can help you build a game. Tell me your idea!")
    
    initial_prompt = input(f"{Fore.GREEN}User: {Style.RESET_ALL}")
    
    # 1. Clarification Phase
    clarifier = Clarifier(api_key, provider)
    print(f"\n{Fore.YELLOW}[Phase 1: Clarification]{Style.RESET_ALL}")
    final_requirements = clarifier.clarify_requirements(initial_prompt)
    if not final_requirements:
        print(f"{Fore.RED}Failed to get requirements.{Style.RESET_ALL}")
        return
        
    print(f"{Fore.YELLOW}Requirements finalized.{Style.RESET_ALL}")
    
    # 2. Planning Phase
    planner = Planner(api_key, provider)
    print(f"\n{Fore.YELLOW}[Phase 2: Planning]{Style.RESET_ALL}")
    game_design_doc = planner.create_plan(final_requirements)
    print(f"{Fore.YELLOW}Plan created.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{game_design_doc}{Style.RESET_ALL}")

    # 3. Execution Phase
    executor = Executor(api_key, provider)
    print(f"\n{Fore.YELLOW}[Phase 3: Execution]{Style.RESET_ALL}")
    print("Generating code...")
    game_files = executor.generate_code(final_requirements, game_design_doc)
    
    # Save files
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    if game_files:
        for filename, content in game_files.items():
            save_file(os.path.join(output_dir, filename), content)
            print(f"Saved {filename}")
    else:
        print(f"{Fore.RED}No files generated.{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}=== Game Generation Complete! ==={Style.RESET_ALL}")
    print(f"Check the '{output_dir}' directory for your game.")

if __name__ == "__main__":
    main()
