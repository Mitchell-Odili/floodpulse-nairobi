from google.adk.tools import ToolContext

def update_mission_context(
    tool_context: ToolContext, 
    responder_name: str, 
    latitude: float, 
    longitude: float
) -> str:
    """
    Saves user-provided mission details into the persistent session state.
    """
    # Write directly to the session state
    tool_context.session.state["responder_name"] = responder_name
    tool_context.session.state["latitude"] = latitude
    tool_context.session.state["longitude"] = longitude
    
    return f"Mission context updated for {responder_name} at {latitude}, {longitude}."