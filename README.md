# 🌊 FloodPulse: Nairobi-First Edge AI

**Offline-First Multi-Agent Resilience for the Mbagathi Basin**

**Mission:** FloodPulse is an autonomous agentic pipeline designed to navigate the Mbagathi Basin during infrastructure failure. We are building the bridge between AI that assists and AI that acts, ensuring Nairobi's residents have a Digital Guardian when the grid goes dark.

---
## 🏗 System Architecture: The "Studio" Pattern

We have transitioned from a multi-level sequential model to a unified Agentic Studio architecture.
- **Level 0 (The Gallery):** A persistent registry for personas (Sarah, Juma, Kamau) and finalized mission assets.
- **Level 1 (The Studio):** The core Agentic Synthesis engine. It orchestrates specialized sub-agents (Vision Analyst, Weather Gatherer, Asset Generator) to synthesize mission-critical data in real-time.
- **Level 2 (Graph Orchestration)**: Google Cloud Spanner backbone for persistent node-based navigation.

---
  
### 📊 Evolutionary Roadmap
| Phase | Milestone | Status |
|-------------|--------|--------------|
| **Level 0** | Identity Factory: Parametric persona generation| ✅ Done |
| **Level 1** | The Studio: Agentic Synthesis & Telemetry Integration | 🟡 Ongoing |
| **Level 2** | Graph Orchestration: Spanner/GQL Navigation | ✅ Done |
| **Edge** | Android 17 Parity: Local Gemma 4 inference | 🔜 Planned |

---

## 🛠 Technical Specifications: The Studio (Level 1)

The `FloodPulseStudio` orchestrator manages the entire lifecycle of a mission request, moving beyond simple scripts to a formal Artifact Promotion Pipeline:

- **FR1 (Asset Synthesis):** The orchestrator synthesizes mission-specific maps upon request using Gemini 2.5/3.5 Flash.
- **FR2 (Telemetry-Aware Synthesis):** Fuses real-time environmental telemetry (Weather) and terrain data (Vision) into a unified risk assessment.
- **FR3 (Artifact Promotion):** Automated pipeline moves validated assets from `/level_0/outputs` to the public `/level_1/assets` registry.
- **FR4 (Memory Injection):** Contextual injection of persona metadata into callback_context to ensure "Persona-Aware" agents.
- **FR5 (Interaction):** Interactive root agent discovery phase to determine mission parameters.
- **FR6 (Idempotency):** Check-before-create logic ensures cost-efficient LLM utilization.

---
## 🧬 Identity & Asset Pipeline (Level 0)
Using **Gemini 3.1 Flash Image (Nano Banana 2)**, we generate consistent cultural markers (e.g., Kenyan-specific beaded bracelets) that persist across portraits and map icons.

- **Orchestrator:** `create_identity.py` (Orchestrator/Worker pattern).
- **Output:** Consistent visual assets stored in `level_0/outputs/.`

---

## 🕸️ Graph Orchestration & Resilience (Level 2)
The system leverages `Google Cloud Spanner` to maintain a live graph of the "Trinity."

- **Relational Intelligence:** `FloodResilienceGraph` maps emergency lifelines between residents and responders.
- **Architectural Resilience:** Implements **Dual-Redundancy DDL**. The system prioritizes local `schema.sql` files but maintains an Internal Hardcoded DDL backup to ensure the database "Brain" can be reconstituted anywhere, even in disconnected environments.
---
## 🎯 Technical Validation: "The Mbagathi Truth"

- **Baseline:** Validated spatial reasoning for topographical analysis (`Gemma 4 (31B)` , `Gemini-2.5-Flash`).
- **Graph Verification:** Confirmed directed pathing from Sarah (Resident) at high-risk sump coordinates to Juma (Responder).
**Data Pivot:** Optimized location data using WKT String format for cross-platform compatibility.
 
### Gemma 4 
We conducted a zero-shot analysis using **Gemma 4 (31B)** on high-resolution satellite imagery to validate core spatial reasoning.

### **Key Findings:**
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
| **Kaggle** | **Data Engineering** | Geospatial Notebooks, NASA SRTM Datasets | 
| **GitHub** | **Source & CI/CD** | Python, Model Context Protocol (MCP) and FastMCP |
| **Google Cloud** | **Production Scale** | Cloud Spanner Graph(Live/Seeded), FastAPI, Cloud Run, WKT (Well-Known Text) Spatial Modeling |
---