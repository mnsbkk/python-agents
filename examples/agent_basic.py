import asyncio              # Required to run asynchronous code (the main event loop)
import os                   # To interact with the operating system (reading environment variables)
from pathlib import Path    # Object-oriented filesystem paths, used to safely locate the .env file

# Import the core Agent class from Microsoft's Agent Framework
from agent_framework import Agent  
# Import the Gemini integration for the Agent Framework
from agent_framework_gemini import GeminiChatClient 
from dotenv import load_dotenv           # To load variables from our .env file
from rich import print                   # A prettier replacement for the standard print()

# --- 1. ENVIRONMENT VARIABLES ---
# Create a Path object pointing to the .env file located one directory up from this script
env_path = Path(__file__).resolve().parent.parent / ".env"
# Load the .env file. override=True ensures it overrides any existing system environment variables
load_dotenv(dotenv_path=env_path, override=True)

# Safety check: Make sure the Google API key is actually loaded before proceeding
if not os.environ.get("GOOGLE_API_KEY"):
    print("[bold red]Error:[/bold red] GOOGLE_API_KEY is not set in your .env file.")
    exit(1) # Exit the script with an error code 1 if the key is missing

# --- 2. INITIALIZE THE AI CLIENT ---
# Initialize the Gemini client. It automatically reads GOOGLE_API_KEY and GOOGLE_MODEL from the environment
client = GeminiChatClient()

# --- 3. CREATE THE AGENT ---
# The Agent acts as the orchestrator. It holds the client and the system instructions.
agent = Agent(
    client=client, # Pass in the Gemini client we created earlier
    # Instructions tell the LLM its persona and how it should behave.
    instructions="You're an informational agent. Answer questions cheerfully."
)

# --- 4. THE MAIN EXECUTION LOOP ---
async def main():
    print("[bold cyan]User Prompt:[/bold cyan] Whats weather today in San Francisco?")
    
    # The agent.run() method is where the magic happens:
    # 1. It packages your text prompt and the "instructions" into a payload.
    # 2. It sends a POST request to the Google Gemini API.
    # 3. It waits asynchronously for Gemini to generate a response.
    # 4. It parses the JSON response and wraps it in an AgentResponse object.
    response = await agent.run("Whats weather today in San Francisco?")
    
    # Extract the actual text string from the response object and print it
    print("\n[bold green]Final Response:[/bold green]")
    print(response.text)

# --- 5. ENTRY POINT ---
if __name__ == "__main__":
    # Start the asyncio event loop and execute the main() function
    asyncio.run(main())