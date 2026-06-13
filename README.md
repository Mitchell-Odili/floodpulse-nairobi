# 🌊 FloodPulse: Edge-to-Cloud Studio

**Autonomous Multi-Agent Resilience for the Mbagathi River Basin**

**Mission:** FloodPulse is an autonomous agentic pipeline designed to navigate the Mbagathi Basin during infrastructure failure. We are building the bridge between AI that assists and AI that acts, ensuring Nairobi's residents have a Digital Guardian when the grid goes dark.

**View the full Specification:** [Read the PRD Spec](docs/PRD.md)

---
## 🏗 System Architecture: The "Studio" Pattern

We have transitioned from a multi-level sequential model to a unified Agentic Studio architecture.
- **The Gallery (Level 0):** A persistent registry for personas (Sarah, Juma, Kamau) and finalized mission assets.
- **The Sandbox:** Our experimental laboratory. This is where we stress-test new MCP tool-calling logic and authenticate secure connections via Application Default Credentials (ADC) before they graduate to the Studio.
- **The Studio (Level 1 ):** The core Agentic Synthesis engine. It utilizes the **Google Agent Development Kit (ADK)** to orchestrate specialized sub-agents (Weather Gatherer, Vision Analyst) through a sequential delegation loop, ensuring atomic state management and session-scoped reliability.
  - **Visualizing the Workflow:** See how the Director manages the Sequential Agentic Loop in our Level 1 Architecture Viz.
![FloodPulse Studio Workflow](docs/level_1_workflow_viz.png)
- **Graph Orchestration (Level 2)**: Google Cloud Spanner backbone for persistent node-based navigation.
  

---
## 📂 Project Structure

``` Plaintext
floodpulse-nairobi/
├── docs/               # Architecture visuals, PRDs, & lab reports
├── levels/
│   ├── level_0/        # The Gallery: Identity & Asset Seeds
│   ├── level_1/        # The Studio: ADK Sequential Orchestration
│   └── level_2/        # Graph Orchestration: Spanner/GQL
├── sandbox/            # Experimental MCP rigs & diagnostic lab
├── tools/              # Shared spatial (map), weather & context tools
├── utils.py            # Global Resilience Layer (Retry logic, shared helpers)
├── config.json         # Global application settings
├── config.py           # Configuration handler & validation
├── pyproject.toml      # Dependency management (uv)
├── uv.lock             # Deterministic lockfile
└── __init__.py             # Package namespace initialization
```
  
### 📊 Evolutionary Roadmap
| Phase | Milestone | Status |
|-------------|--------|--------------|
| **Level 0** | Identity Factory: Parametric persona generation| ✅ Done |
| **Sandbox** | MCP Lab: Secure Vision/Tool Diagnostics | ✅ Done | 
| **Level 1** | The Studio: Agentic Synthesis & Telemetry Integration | ✅ Done |
| **Level 2** | Graph Orchestration: Spanner/GQL Navigation | 🟡 Ongoing |
| **Edge** | Android 17 Parity: Local Gemma 4 inference | 🔜 Planned |
---
## 🛡️ Resilience & State Protocol
- **Resilience Layer (`utils.p`y):** We use `@http/genai_retry` decorators across all API-bound tools (Maps, Weather, GenAI). They utilizes exponential backoff with jitter to gracefully recover from `429 (Resource Exhausted)` and `503 (Unavailable) errors`.
- **Context-Setter Pattern:** The Director agent uses the `update_mission_context` tool to persist mission parameters (Name, Lat, Lon) into `tool_context.session.state`. This ensures that downstream agents have reliable access to validated mission data.
-**Asset Caching:** To preserve daily API quotas, all map and terrain assets are checked against the local `/assets/` directory before triggering remote API calls.
---

## ⚙️ Setup & Execution
1. **Install Dependencies:** `uv sync`
2. **Environment Variables:** Create a `.env` file in the project root:
```plaintext
# API Keys (For Sandbox / Prototyping)
GEMINI_API_KEY=
MAPS_API_KEY=
OPENWEATHER_API_KEY=

# ADC / Vertex AI (For Production Studio)
USE_VERTEX_AI=true
PROJECT_ID=your-project-id
LOCATION=us-central1
```
3. **Authentication Protocol**

The system supports two execution modes via `config.py`:
- **Sandbox Mode (`USE_VERTEX_AI=false`):** Uses standard API keys. Ideal for rapid iteration, testing, and debugging.
- **Studio Production Mode (`USE_VERTEX_AI=true`):** Uses **Application Default Credentials (ADC)**. This leverages your project's IAM identity for secure, enterprise-grade access.
  - **Note:** Ensure you have authenticated locally via `gcloud auth application-default login` before running in Studio mode.
    
4. **Run Missions:** Execute from the root directory using the module flag:
```
uv run python -m levels.level_1.agent
adk web levels/level_1 
```
---
## 🎯 Technical Validation: "The Mbagathi Truth"

- **Baseline:** Validated spatial reasoning for topographical analysis (`Gemma 4 (31B)` , `Gemini-2.5-Flash`, `Gemini-3.5-Flash`).
- **MCP Diagnostics:** Validated tool-calling reliability via the MCP Inspector, ensuring our agents can "see" map assets locally even when cloud-disconnected.
- **Safe Ridge Logic:** The model autonomously identifies high-ground zones based on spectral terrain analysis (elevation vs. drainage).
- **Graph Verification:** Confirmed directed pathing from Sarah (Resident) at high-risk sump coordinates to Juma (Responder).
> **Status:** ✅ Feasibility Confirmed. Our hybrid Edge-to-Cloud Studio pattern provides the necessary spatial intuition for urban flood navigation.
---
## 🧠 Gemma 4 
We conducted a zero-shot analysis using **Gemma 4 (31B)** on high-resolution satellite imagery to validate:.
* **River Path:** Successfully identified the riparian corridor despite urban canopy cover.
* **Critical Nodes:** Pinpointed three high-risk intersections:
    1. **Lang'ata Road/ICC Crossing:** Identified as a primary arterial bottleneck.
    2. **South B/C Border:** Identified as a "low-water" neighborhood split-point.
    3. **Lower Basin Sumps:** Corrected identified as high-risk vehicle entrapment zones.
* **Safe Ridge Logic:** The model autonomously identified the **South B Plateau** as a primary evacuation zone based on spectral terrain analysis (elevation vs. drainage).

> **Status:** ✅ Feasibility Confirmed. The model demonstrates the required spatial intuition for urban flood navigation.

---
## 🛠️ The Tech Stack: The Path to Production
We leverage a hybrid stack that moves from rapid AI prototyping to high-scale cloud infrastructure.

| Environment | Purpose | Core Technologies |
|-------------|---------|-------------------|
| **AI Studio** | **Prototyping** | Gemma 4 31B (Multimodal Reasoning) |
| **Sandbox** | **MCP Validation** | FastMCP, Inspector, ADC Authentication |
| **Vertex AI** | **Orchestration** | **Google ADK (SequentialAgent)**, Gemini 2.5/3.5 Flash, Gemini 3.1 Flash Image (Visual Asset Generation) |
| **Google Cloud** | **Production Scale** | Cloud Spanner Graph(Live/Seeded), FastAPI, Cloud Run, WKT (Well-Known Text) Spatial Modeling |
---