# level_3/agents/orchestrator.py
from config import MODELS
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import AgentTool
from levels.level_3.agents.sub_agents.risk_analyst import risk_analyst
from levels.level_3.agents.sub_agents.mission_ops import mission_ops

# floodpulse_pipeline = SequentialAgent(
#     name="FloodPulse_Workflow",
#     sub_agents=[risk_analyst, mission_ops],
#     description="Sequentially evaluates basin telemetry via the Risk Analyst and executes response and rescue actions via Mission Operations."
# )

risk_analyst_tool = AgentTool(agent=risk_analyst)


floodpulse_director = Agent(
    name="Mbagathi_Basin_Director",
    model=MODELS["director"],
    tools=[risk_analyst_tool],
    sub_agents=[mission_ops],
    instruction="""
    You are Kamau, the Director of FloodPulse, managing emergency operations in the Mbagathi Basin.
    
    CORE WORKFLOW & RULES:
    1. **Execute Telemetry Checks & Lookups:** When asked about basin-wide risk, general node statuses, 
    or looking up individual people/entities by name (e.g., "Where is Sarah?"), invoke the `risk_analyst_tool`.
    2. **Synthesize, Don't Dump:** Read the structured assessment returned by the tool internally. Translate it
     into a concise, authoritative operational briefing for the user.
    3. **Strict Text Output:** Never output raw JSON, dictionaries, or code blocks. Speak purely as Director Kamau
     in plain text.
    4. **Delegate Operations:** For rescue, routing, dispatching help, and finalization tasks, delegate execution strictly to `mission_ops_tool`.
    """,
)