import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Path patching to ensure the 'levels' module is visible from the root
root_dir = Path(__file__).resolve().parents[2]
sys.path.append(str(root_dir))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types, Client

from levels.level_3.simulation.hydrological_terrain import run_basin_impact_simulation
from levels.level_3.agents.orchestrator import floodpulse_director

load_dotenv()

async def run_mission():
    # 1. Initialize Basin Data (Simulation & Telemetry Refresh) with actual environment variables
    print("🌊 Running hydrological basin simulation...")
    run_basin_impact_simulation(
        project_id=os.getenv("PROJECT_ID"),
        instance_id=os.getenv("SPANNER_INSTANCE_ID"),
        database_id=os.getenv("SPANNER_DATABASE_ID"), 
        storm_center_lat=-1.3200, 
        storm_center_lon=36.8150
    )

    # 2. Setup Agent Session
    # Context is injected here; the agents will query Spanner using these IDs
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="floodpulse_app",
        user_id="user_01",
        session_id="session_01",
        metadata={
            "resident_id": "node_001",    # Sarah
            "responder_id": "node_002",   # Juma
            "authority_name": "Kamau"     # Director Persona
        }
    )
    
    # 3. Initialize Runner with the Director
    runner = Runner(
        app_name="floodpulse_app",
        agent=floodpulse_director,
        session_service=session_service,
    )

    print("🚀 FloodPulse Mission Control Online")
    print("--- Starting Agentic Orchestration ---")

    # Initial prompt to trigger the Director's greeting and status report
    user_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text="Report for duty. What is the current status of the basin?")]
    )

    # 4. Run Mission Loop
    # The agent will now interact with you, potentially asking for confirmation
    for update in runner.run(
        session_id="session_01",
        user_id="user_01",
        new_message=user_message
    ):
        print(update)

    # 5. Capture Results
    final_session = await session_service.get_session("session_01")
    mission_data = final_session.metadata.get("mission_data")

    if mission_data:
        print(f"\n--- Mission Data Captured ---")
        print(f"Final Decision: {mission_data.get('final_verdict')}")

    print("--- Mission Complete ---")

if __name__ == "__main__":
    asyncio.run(run_mission())