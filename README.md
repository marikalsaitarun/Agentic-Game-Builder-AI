# Agentic Game-Builder AI

An intelligent agent that designs and generates playable HTML/CSS/JS games from natural language descriptions. This project demonstrates an agentic workflow using LLMs (OpenAI or Google Gemini) to clarify requirements, plan architecture, and execute code generation.

## 🏗️ Architecture

The agent follows a structured **Chain-of-Thought** process, divided into three distinct phases:

1.  **Clarification Agent (`Clarifier`)**:
    *   Interacts with the user to refine the initial game idea.
    *   Asks targeted questions until it has a clear set of requirements.
    *   Output: Finalized Requirements.

2.  **Planning Agent (`Planner`)**:
    *   Takes the finalized requirements and creates a comprehensive Game Design Document (GDD).
    *   Outlines game mechanics, UI structure, and technical implementation details.
    *   Output: Game Design Document.

3.  **Execution Agent (`Executor`)**:
    *   Reads the GDD and requirements.
    *   Generates the actual source code (`index.html`, `style.css`, `game.js`).
    *   Output: Working game files in the `output/` directory.

The system uses a unified `LLMClient` to interface with either OpenAI's GPT-4o or Google's Gemini models (default: `gemini-2.5-flash-lite`), allowing for flexibility in backend selection.

## 🚀 How to Run

### Option 1: Docker (Recommended)

Packaging the agent in Docker ensures a consistent environment.

#### Method A: Pull from Docker Hub (Fastest)

The image is available on Docker Hub: [saitarunmarikal/agentic-game-builder](https://hub.docker.com/r/saitarunmarikal/agentic-game-builder)

1.  **Pull the image:**
    ```bash
    docker pull saitarunmarikal/agentic-game-builder:latest
    ```

2.  **Run the container:**
    ```bash
    # Using .env file (Recommended)
    docker run -it --env-file .env -v ${PWD}/output:/app/output saitarunmarikal/agentic-game-builder:latest
    
    # OR manually passing the key
    docker run -it -e GEMINI_API_KEY=your_key -v ${PWD}/output:/app/output saitarunmarikal/agentic-game-builder:latest
    ```

#### Method B: Build from Source

1.  **Build the Docker image:**
    ```bash
    docker build -t game-builder .
    ```

2.  **Run the built image:**
    You must pass your API key as an environment variable and mount a volume to retrieve the generated files.

    **For OpenAI Users:**
    ```bash
    docker run -it -e OPENAI_API_KEY=your_key_here -v $(pwd)/output:/app/output game-builder
    ```

    **For Google Gemini Users:**
    ```bash
    docker run -it -e GEMINI_API_KEY=your_key_here -v $(pwd)/output:/app/output game-builder
    ```

    *Note: The `-it` flag is crucial as the agent requires interactive input from the user.*
    *Note: On Windows PowerShell, use `${PWD}` instead of `$(pwd)`.*

    **Alternative (Easier): Use .env file**
    If you have a `.env` file with your keys, you can simply run:
    ```bash
    docker run -it --env-file .env -v ${PWD}/output:/app/output game-builder
    ```

### Option 2: Local Python

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set Environment Variables:**
    Create a `.env` file in the root directory:
    ```env
    OPENAI_API_KEY=your_key
    # OR
    GEMINI_API_KEY=your_key
    ```

3.  **Run the agent:**
    ```bash
    python main.py
    ```

## ⚖️ Trade-offs

*   **Single-Pass Generation**: The current execution phase generates all code in one go. If there's a syntax error or logic bug, the agent doesn't have a feedback loop to fix it automatically.
*   **Context Window Management**: The conversation history in the clarification phase is appended linearly. For extremely long conversations, this could hit token limits, though modern models usually handle this well.
*   **No State Persistence**: The agent doesn't save the state of the conversation between runs. If the process is interrupted, you must start over.
*   **CLI Interface**: A command-line interface was chosen for simplicity and ease of containerization, but a Web UI would offer a better user experience for game previewing.

## 🔮 Future Improvements

With more time, the following enhancements would be prioritized:

1.  **Self-Correction Loop**: Implement a "Reviewer" agent that runs the generated code (or lints it) and feeds errors back to the Executor for fixing.
2.  **Web-Based Interface**: Create a Streamlit or React frontend to allow users to play the generated game immediately within the same interface.
3.  **Asset Generation**: Integrate an image generation model (like DALL-E 3 or Imagen) to create custom sprites and backgrounds instead of using CSS shapes or placeholders.
4.  **Project Scaffolding**: Support more complex project structures (e.g., separating JS into modules, using a bundler like Vite) for larger games.
5.  **Unit Testing**: Add a suite of tests to verify the agent's internal logic and prompt effectiveness.
