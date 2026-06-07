# 🌊 FloodPulse: Nairobi-First Edge AI

**Offline-First Multi-Agent Resilience for the Mbagathi Basin**

**Mission:** FloodPulse is an autonomous agentic pipeline designed to navigate the Mbagathi Basin during infrastructure failure. We are building the bridge between AI that assists and AI that acts, ensuring Nairobi's residents have a Digital Guardian when the grid goes dark.

**View the full Specification:** [Read the PRD Spec](docs/PRD.md)

---
## 🏗 System Architecture: The "Studio" Pattern

We have transitioned from a multi-level sequential model to a unified Agentic Studio architecture.
- **Level 0 (The Gallery):** A persistent registry for personas (Sarah, Juma, Kamau) and finalized mission assets.
- **Level 1 (The Studio):** The core Agentic Synthesis engine. It orchestrates specialized sub-agents (Vision Analyst, Weather Gatherer, Asset Generator) to synthesize mission-critical data in real-time.
- **Level 2 (Graph Orchestration)**: Google Cloud Spanner backbone for persistent node-based navigation.
---
## 📂 Project Structure

``` Plaintext
floodpulse-nairobi/
├── data/               # Persistent mission registry
├── docs/               # Architecture visuals, PRDs, & design docs
├── levels/
│   ├── level_0/        # The Gallery: Identity & Asset Seeds
│   ├── level_1/        # The Studio: Agentic Synthesis
│   └── level_2/        # Graph Orchestration: Spanner/GQL
├── utils/              # State management & utilities
├── config.json         # Global application settings
├── config.py           # Configuration handler & validation
├── pyproject.toml      # Dependency management (uv)
└── uv.lock             # Deterministic lockfile
```
  
### 📊 Evolutionary Roadmap
| Phase | Milestone | Status |
|-------------|--------|--------------|
| **Level 0** | Identity Factory: Parametric persona generation| ✅ Done |
| **Level 1** | The Studio: Agentic Synthesis & Telemetry Integration | ✅ Done |
| **Level 2** | Graph Orchestration: Spanner/GQL Navigation | 🟡 Ongoing |
| **Edge** | Android 17 Parity: Local Gemma 4 inference | 🔜 Planned |
---
## 🎯 Technical Validation: "The Mbagathi Truth"

- **Baseline:** Validated spatial reasoning for topographical analysis (`Gemma 4 (31B)` , `Gemini-2.5-Flash`, `Gemini-3.5-Flash`).
- **Graph Verification:** Confirmed directed pathing from Sarah (Resident) at high-risk sump coordinates to Juma (Responder).
**Data Pivot:** Optimized location data using WKT String format for cross-platform compatibility.
 
### Gemma 4 
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
| **Vertex AI** | **Orchestration** | Gemini 2.5/3.5 Flash (Agentic Loops & Reasoning), Gemini 3.1 Flash Image (Visual Asset Generation) |
| **GitHub** | **Source & CI/CD** | Python, Model Context Protocol (MCP) and FastMCP |
| **Google Cloud** | **Production Scale** | Cloud Spanner Graph(Live/Seeded), FastAPI, Cloud Run, WKT (Well-Known Text) Spatial Modeling |
---