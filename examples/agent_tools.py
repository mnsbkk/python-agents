import asyncio              # Required to run asynchronous code (the main event loop)
import logging              # Standard library for logging
import os                   # To interact with the operating system (reading environment variables)
import random               # Used to generate random numbers for our fake weather tool
import sys                  # Used to access system-specific parameters and functions (like command-line args)
from datetime import datetime  # To get the current date for the date tool
from pathlib import Path    # Object-oriented filesystem paths, used to locate the .env file safely
from typing import Annotated
from pydantic import Field

# Import the core components from Microsoft's Agent Framework
from agent_framework import Agent, tool  # 'Agent' is the orchestrator, 'tool' is a decorator to expose Python functions to the LLM
# Import the Gemini integration for the Agent Framework
from agent_framework_gemini import GeminiChatClient 
from dotenv import load_dotenv           # To load variables from our .env file
from rich import print                   # A prettier replacement for the standard print()
from rich.logging import RichHandler     # A prettier log handler for the terminal

# --- 1. SETUP LOGGING ---
# Create a custom log handler that formats logs nicely in the terminal
handler = RichHandler(show_path=False, rich_tracebacks=True, show_level=False)
# Configure the global logging system to use our RichHandler
logging.basicConfig(level=logging.WARNING, handlers=[handler], force=True, format="%(message)s")
# Get a logger instance for this specific script
logger = logging.getLogger(__name__)
# Set the log level to INFO so we can see when our tools are called by the AI
logger.setLevel(logging.INFO)

# --- 2. ENVIRONMENT VARIABLES ---
# Create a Path object pointing to the .env file located one directory up from this script
env_path = Path(__file__).resolve().parent.parent / ".env"
# Load the .env file. override=True ensures it overrides any existing system environment variables
load_dotenv(dotenv_path=env_path, override=True)

# Safety check: Make sure the Google API key is actually loaded before proceeding
if not os.environ.get("GOOGLE_API_KEY"):
    print("[bold red]Error:[/bold red] GOOGLE_API_KEY is not set in your .env file.")
    sys.exit(1) # Exit the script with an error code 1

# --- 3. INITIALIZE THE AI CLIENT ---
# Initialize the Gemini client. It automatically reads the GOOGLE_API_KEY and GOOGLE_MODEL from the environment
client = GeminiChatClient()


# --- 4. DEFINE THE TOOLS (FUNCTIONS THE AI CAN CALL) ---
# The @tool decorator automatically parses the function signature, type hints, and docstrings
# and converts them into the JSON Schema that Gemini expects.

@tool
def get_weather(
    city: Annotated[str, Field(description="The city to get the weather for.")]
    ) -> dict:
    """Returns weather data for a given city, a dictionary with temperature and description.
    
    Args:
        city: The city to get the weather for.
    """
    # Log that the AI successfully triggered this tool
    logger.info(f"Getting weather for {city}")
    
    # Randomly return Sunny (5% chance) or Rainy (95% chance) to make the agent's logic dynamic
    if random.random() < 0.05:
        return {
            "temperature": 72,
            "description": "Sunny",
        }
    else:
        return {
            "temperature": 60,
            "description": "Rainy",
        }


@tool
def get_activities(
    city: Annotated[str, Field(description="The city to get activities for.")],
    date: Annotated[str, Field(description="The date to get activities for in format YYYY-MM-DD.")],
) -> list[dict]:
    """Returns a list of activities for a given city and date.
    
    Args:
        city: The city to get activities for.
        date: The date to get activities for in format YYYY-MM-DD.
    """
    logger.info(f"Getting activities for {city} on {date}")
    # Return a dummy list of activities
    return [
        {"name": "Hiking", "location": city},
        {"name": "Beach", "location": city},
        {"name": "Museum", "location": city},
    ]


@tool
def get_current_date() -> str:
    """Gets the current date from the system and returns as a string in format YYYY-MM-DD."""
    logger.info("Getting current date")
    # The LLM doesn't know today's date, so it must call this tool if the user asks about "this weekend"
    return datetime.now().strftime("%Y-%m-%d")


# --- 5. CREATE THE AGENT ---
# The Agent acts as the orchestrator. It holds the client, the system instructions, and the tools.
agent = Agent(
    client=client, # Pass in the Gemini client we created earlier
    name="weekend-planner", # An identifier for the agent
    
    # System instructions tell the LLM its persona, constraints, and how it should behave.
    # It explicitly tells the LLM to check the weather before suggesting activities.
    instructions=(
        "You help users plan their weekends and choose the best activities for the given weather. "
        "If an activity would be unpleasant in weather, don't suggest it. Include date of the weekend in response."
    ),
    
    # We give the agent access to the three functions we defined above.
    tools=[get_weather, get_activities, get_current_date], 
)


# --- 6. THE MAIN EXECUTION LOOP ---
async def main():
    # The agent.run() method handles the entire ReAct (Reasoning and Acting) loop automatically:
    # 1. It sends the user prompt + tool definitions to Gemini.
    # 2. Gemini responds with a request to call one or more tools (e.g., "Call get_current_date").
    # 3. The framework executes the Python function and sends the result back to Gemini.
    # 4. This repeats until Gemini decides it has enough info to generate a final text response.
    
    print("[bold cyan]User Prompt:[/bold cyan] what can I do this weekend in San Francisco?")
    response = await agent.run("what can I do this weekend in San Francisco?")
    
    # Print the final natural language response generated by Gemini
    print("\n[bold green]Final Response:[/bold green]")
    print(response.text)


# --- 7. ENTRY POINT ---
if __name__ == "__main__":
    # Check if the user passed the "--devui" flag in the terminal
    if "--devui" in sys.argv:
        # DevUI is an experimental web interface for interacting with agents.
        from agent_framework.devui import serve
        # serve() starts a local web server and auto-opens the browser
        serve(entities=[agent], auto_open=True, auth_enabled=False)
    else:
        # Standard CLI execution: Start the asyncio event loop and run our main() function
        asyncio.run(main())