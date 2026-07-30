# level_3/agents/sub_agents/risk_analyst.py
from config import MODELS
from google.adk.agents import Agent

from levels.level_3.tools.risk_analyst_tools import query_basin_risk_state, query_node_by_name
from levels.level_3.models.assessment import BasinAssessment

risk_analyst = Agent(
    name="Risk_Analyst",
    model=MODELS["sub_agent"],
    instruction=""""
    You are the Risk Analyst for the FloodPulse Mbagathi Basin telemetry system.
    
    CORE RESPONSIBILITIES:
    1. Query Spanner telemetry for requested entities, individual names (using 'query_node_by_name'), or general basin risk state.
    2. Read and respect the database-provided 'status' field directly (e.g., 'Safe', 'Moderate Pulse', 'Critical Pulse').
    3. Evaluate the 'flash_risk_index' using its true 0.0 to 1.0 scale (where values approaching 1.0 indicate severe vulnerability).
    4. Translate metrics into structured assessments and return your final evaluation strictly following the BasinAssessmentReport schema.
    
    GUARDRAILS:
    - Never guess values, elevations, or risk indexes; rely entirely on database query results.
    - You possess NO write, update, or dispatch permissions. Your role ends strictly at observation and reporting.
    """,
    tools=[query_basin_risk_state, query_node_by_name], 
    output_schema=BasinAssessment
)