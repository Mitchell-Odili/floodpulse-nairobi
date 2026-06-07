# levels/level_1/__init__.py
import sys
from pathlib import Path

# Add the project root (the folder containing 'levels/') to the path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

# 3. Now you can safely import your agents/tools
from .agents.orchestrator import floodpulse_director as root_agent

__all__ = ["root_agent"]