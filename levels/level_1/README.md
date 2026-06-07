# 🌊 FloodPulse Nairobi: Studio Engine

FloodPulse Nairobi is an autonomous agentic synthesis engine designed for real-time flood risk assessment in the Mbagathi River Basin. Moving beyond linear scripts, the system employs a "Studio Architecture" that orchestrates specialized AI agents to perceive, reason, and act within dynamic geospatial environments.

To support this mission, our **Sandbox** provides an ephemeral laboratory for testing MCP-based vision tools and agentic logic, ensuring every new capability is rigorously validated before integration into the core engine.

---
## 🏗️ Studio Architecture

The system is built on an **Agentic Interaction Loop:**

1. **Perception:** Parallel telemetry gathering via satellite vision and environmental weather sensors.
2. **Reasoning:** A Director agent synthesizes multi-sensor data into safety directives.
3. **Action:** Dynamic mapping and risk-overlay generation.
4. **Validation (Sandbox):** Isolated MCP-based testing of perception and tool-calling logic.
5. **Persistence:** Idempotent state management via a central registry.

**View the full architecture:** [Read the Studio Specification](spec.md)

---

## 🚀 Technical Stack
- **Intelligence:** `Google Gemini 2.5 Flash`/`Gemini 3.5 Flash` via `google-genai` SDK.
- **Orchestration:** Multi-agent delegation with parallel thread execution.
- **MCP (Sandbox):** FastMCP for protocol-based tool development and Inspector-based diagnostics.
- **Geospatial:** Google Static Maps API with dynamic icon layering.
- **Telemetry:** OpenWeather API for real-time environmental risk indexing.
- **State Management:** Local `registry.json` for task idempotency and offline-resilient operations.

---

## 📂 Project Structure

``` Plaintext
floodpulse-nairobi/
├── data/               # Persistent mission registry
├── docs/               # Architecture visuals, PRDs, and lab reports
├── levels/             # Core Engine
│   └── level_1/        # Orchestrator & Studio Logic
├── sandbox/            # Experimental MCP rigs & diagnostic lab
├── tools/              # Shared spatial (map) & weather tools
├── utils/              # State management & utility helpers
├── config.json         # Centralized application settings
├── config.py           # Model and API configurations
├── pyproject.toml      # Dependency management & project metadata
└── uv.lock             # Deterministic dependency lockfile
```

### 🛠️ Key Features
- **Parallel Execution:** Orchestrator triggers Weather and Vision agents simultaneously, reducing mission latency.
- **Sandbox Testing:** Dedicated environment for verifying MCP vision tools via the Inspector, ensuring reliable tool-calling before production deployment.
**Idempotency:** Automated path verification and registry checks prevent redundant API calls.
- **Studio Loop:** A centralized FloodPulseStudio class handles the lifecycle of every request, ensuring consistent persona and context maintenance.

---

## 📍 Deployment Nodes
The system currently manages the "Trinity" nodes in the Mbagathi Basin:

- **Sarah:** T-Mall Underpass (The Sump Observer)
- **Juma:** Lang'ata/ICC (The Arterial Responder)
- **Kamau:** Madaraka/Highview (The Ridge Strategist)

---

## ⚙️ Setup & Configuration
1. **Environment Variables**: Create a `.env` file in the project root and populate the following keys:

- `Maps_API_KEY`: Your Google Static Maps API key.
- `OPENWEATHER_API_KEY`: Your OpenWeather API key.
- `GEMINI_API_KEY`: Your Google GenAI API key.

2. **Install Dependencies**: Run `uv sync` to ensure all requirements are met from your virtual environment.
3. **Initialize**: Instantiate the FloodPulseStudio via `orchestrator.py`.
4. **Execute:** Run missions using the run_mission(user_input, responder_name) entry point.
5. **Experiment:** Explore the `sandbox/` folder to run diagnostic tests using the MCP Inspector.
---
*Developed for Mbagathi Basin Flood Resilience | Level 1: Terrain Discovery & Pinpointing*