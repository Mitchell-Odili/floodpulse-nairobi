# level_3/sub_agents/mission_ops.py
from config import MODELS
from google.adk.agents import Agent
from levels.level_3.tools.mission_ops_tools import get_nearest_responder, calculate_rescue_route, dispatch_to_resident, finalize_rescue
from levels.level_3.models.mission import RescuePlan

mission_ops = Agent(
    name="Mission_Operations",
    model=MODELS["sub_agent"],
    instruction=""""
    You are the Mission Operations lead. 
    1. Receive critical node/resident targets from the Director.
    2. Use 'get_nearest_responder' to locate the closest available unit.
    3. Use 'calculate_rescue_route' to map out safe evacuation paths avoiding high-risk edges.
    4. Execute 'dispatch_to_resident' to lock database states and launch the mission.
    5. Execute 'finalize_rescue' once operations are complete to restore states to Clear/Safe.
    6. Output a structured 'RescuePlan' reflecting these operations.
    """,
    tools=[
        get_nearest_responder, 
        calculate_rescue_route, 
        dispatch_to_resident, 
        finalize_rescue
    ],
    # response_schema=RescuePlan
)