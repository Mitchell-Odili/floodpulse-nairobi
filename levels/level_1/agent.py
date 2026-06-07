"""
Level 1: FloodPulse Entry Point (ADK Bridge)
Connects the ADK interface to our modular Orchestrator.
"""

from .agents.orchestrator import floodpulse_director as root_agent

# The ADK looks for 'root_agent' by name. 
# By importing our orchestrator as root_agent, we maintain 
# compatibility without duplicating code.

__all__ = ["root_agent"]