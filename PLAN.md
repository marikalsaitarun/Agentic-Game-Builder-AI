# Implementation Plan: Dockerized Agentic Game Builder

This document outlines the plan to package the Agentic Game Builder into a deployable Docker container with comprehensive documentation.

## 1. Objective
Package the existing Python-based agent into a Docker container to ensure consistent execution across different environments, and provide clear documentation for users to build and run the agent.

## 2. Deliverables
- **Dockerfile**: A streamlined Dockerfile to build the image.
- **README.md**: Updated documentation with build/run instructions, architecture overview, trade-offs, and future improvements.
- **Codebase**: The existing Python source code (`main.py`, `agent/`, etc.) structured for containerization.

## 3. Implementation Steps

### Step 1: Containerization verification
- Review existing `Dockerfile`.
- Ensure base image (`python:3.11-slim`) is appropriate for size and compatibility.
- Verify `requirements.txt` includes all necessary dependencies (`google-genai`, `openai`, `python-dotenv`, `colorama`).
- Confirm `WORKDIR` and `COPY` instructions correctly place source code.

### Step 2: Documentation (README.md)
- **Architecture Section**:
  - Describe the 3-stage pipeline: Clarifier -> Planner -> Executor.
  - Explain the dual-provider support (OpenAI & Gemini).
- **Usage Instructions**:
  - Add explicit `docker build` command.
  - Add explicit `docker run` commands for both OpenAI and Gemini, highlighting the need for `-it` (interactive mode) and volume mounting for output.
- **Trade-offs & Improvements**:
  - Document current limitations (CLI-only, lack of iterative feedback loop).
  - List planned improvements (Web UI, self-correction, asset generation, unit tests).

### Step 3: configuration Refinement
- Ensure `main.py` correctly handles API keys from environment variables passed via Docker.
- Verify the default Gemini model passed to `LLMClient` reflects the latest update (`gemini-2.5-flash-lite`).

## 4. Verification
- The user should be able to run:
  ```bash
  docker build -t game-builder .
  docker run -it -e GEMINI_API_KEY=... -v $(pwd)/output:/app/output game-builder
  ```
- The agent should start, prompt for input, and generate game files in the mounted `output` directory.
