import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Reliable Pathing: Resolve the root relative to this file
# This works regardless of where you call the script from
PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

# 2. Now imports will work cleanly because PROJECT_ROOT is in sys.path
from levels.level_1.agents.orchestrator import run_mission

if __name__ == "__main__":
    # Test your mission logic
    print("🚀 FloodPulse Mission Control Online")
    result = run_mission("juma", -1.3165, 36.8135)
    print(result)