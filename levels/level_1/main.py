import asyncio
import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from levels.level_1.agents.orchestrator import floodpulse_director

load_dotenv()

async def run_mission():
    session_service = InMemorySessionService()
    
    await session_service.create_session(
        app_name="floodpulse_app",
        user_id="user_01",
        session_id="session_01"
    )
    
    runner = Runner(
        app_name="floodpulse_app",
        agent=floodpulse_director,
        session_service=session_service
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text="Juma at -1.3165, 36.8135 needs an assessment.")]
    )

    print("--- Starting Mission ---")
    # Change 'async for' to 'for' because the runner returns a synchronous generator
    for update in runner.run(
        session_id="session_01",
        user_id="user_01",
        new_message=user_message
    ):
        print(update)
    print("--- Mission Complete ---")

if __name__ == "__main__":
    print("🚀 FloodPulse Mission Control Online")
    # Start the async event loop
    asyncio.run(run_mission())