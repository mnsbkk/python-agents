# Python AI Agents

This repository is a compact learning project that demonstrates how to build AI agents in Python using the Microsoft Agent Framework with Google Gemini models. The examples are intentionally simple and focused on the core patterns used in agent-based applications: creating an agent, connecting it to a model, exposing tools, and letting the model decide when to use them.

The project is not a full application framework or packaged library; it is a small set of runnable examples that show the building blocks for agent workflows.

## What is in this project?

The repository currently contains three example scripts in the `examples/` folder:

- `examples/agent_basic.py` — the simplest possible agent setup.
- `examples/agent_tool.py` — a single-tool agent that can answer weather-related queries by calling a local Python function.
- `examples/agent_tools.py` — a more advanced agent that exposes multiple tools and can plan weekend activities using the current date and weather results.

## Project structure

```text
python-agents/
├── .env
├── .venv/
├── README.md
└── examples/
    ├── agent_basic.py
    ├── agent_tool.py
    └── agent_tools.py
```

## Technologies used

- Python 3.14
- Microsoft Agent Framework (`agent_framework`)
- Gemini integration (`agent_framework_gemini`)
- Google Gemini model API
- `python-dotenv` for environment variables
- `rich` for better terminal output
- `pydantic` for structured tool input definitions

## Prerequisites

Before running the examples, make sure you have:

- Python 3.14 or newer
- A Google Gemini API key
- Access to the internet from the environment where the script runs

## Setup

1. Create and activate a virtual environment:

```bash
cd python-agents
python -m venv .venv
source .venv/bin/activate
```

2. Install the required dependencies:

```bash
python -m pip install agent-framework agent-framework-gemini python-dotenv rich pydantic
```

3. Configure your environment variables in the repo root `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
GOOGLE_MODEL=gemini-3.5-flash-lite
```

The examples use `dotenv` to load this file automatically.

## Running the examples

### 1. Basic agent

```bash
python examples/agent_basic.py
```

This script creates a minimal `Agent` and asks Gemini a simple informational question.

### 2. Single tool agent

```bash
python examples/agent_tool.py
```

This example defines a `get_weather()` tool and allows the model to choose whether to call it when answering a weather question.

### 3. Multi-tool weekend planner

```bash
python examples/agent_tools.py
```

This script exposes multiple tools for weather, activities, and date lookup. The agent uses them together to suggest weekend plans while taking the weather into account.

### 4. Dev UI mode

```bash
python examples/agent_tools.py --devui
```

This launches the experimental Agent Framework Dev UI so you can interact with the agent in a browser-based UI.

## How the examples work

The core pattern in all three scripts is the same:

- Instantiate a `GeminiChatClient`
- Create an `Agent` with model instructions and optional tools
- Call `await agent.run(...)`
- Let the framework handle the reasoning and tool-calling loop

Tools are declared with the `@tool` decorator. Each tool is exposed to the model as a callable function with structured parameters, and the framework automatically manages the execution loop between the model and Python code.

## Notes

- The project is designed for experimentation and education.
- The scripts intentionally use mock or simple tool outputs rather than real production integrations.
- The `.env` file contains environment configuration and should not be shared publicly if it contains live credentials.

## Next steps

Once you understand these examples, you can expand the project by adding:

- More domain-specific tools
- External service integrations (APIs, databases, search)
- Persistent memory or conversation state
- A web UI or API layer around the agent
- Better error handling and validation
