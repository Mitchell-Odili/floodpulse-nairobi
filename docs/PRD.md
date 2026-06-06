# 📄 Product Requirements Document: FloodPulse (Nairobi)
**Project Code:** FP-NBO-2026

## 1. Problem Statement
Existing navigation tools in Nairobi rely on static road data and active internet. During flash floods in the Mbagathi basin, infrastructure fails rapidly. Users lack a real-time, offline-first tool to identify "Ground Truth" hazards and find high-ground ridges.

## 2. Goals & Objectives
- **Goal:** Reduce transit-related flood fatalities by 50% in pilot areas.
- **Objective:** Deploy a multimodal agentic pipeline capable of identifying flood boundaries and safe transit paths.
- **Strategic Metric:** Maintain high-fidelity spatial reasoning via Gemini 3.5 and orchestrate reliable navigation directives through modular agentic pipelines.

## 3. System Architecture
FloodPulse utilizes a Modular Agentic Simulation pattern, evolving from static identity creation (Level 0) into a real-time Production Studio (Level 1) for agentic assets.

- **Level 0 (The Gallery):** A persistent registry for personas (Sarah, Juma, Kamau) and finalized mission assets.
- **Level 1 (The Studio):** The core Agentic Synthesis engine. It orchestrates specialized sub-agents (Vision Analyst, Weather Gatherer, Asset Generator) to synthesize mission-critical data in real-time.
- **Level 2 Graph Orchestration:** Google Cloud Spanner backbone for persistent node-based navigation.

### 3.1 Evolutionary Roadmap
| Phase | Milestone | Status |
|-------------|--------|--------------|
| **Level 0** | Identity Factory: Parametric persona generation| ✅ Done |
| **Level 1** | The Studio: Agentic Synthesis & Telemetry Integration | 🟡 Ongoing |
| **Level 2** | Graph Orchestration: Spanner/GQL Navigation | ✅ Done |
| **Edge** | Android 17 Parity: Local Gemma 4 inference | 🔜 Planned |

## 4. Technical Specifications
### 4.1 Level 0: The Gallery (Completed)
- Model: Gemini 3.1 Flash Image (Nano Banana 2).
- Logic: Implemented `create_identity.py` and `generator.py` using an Orchestrator/Worker pattern.
- Output: Consistent visual assets stored in `level_0/outputs/.`

### 4.2 Level 1: The Studio (Ongoing)
- **FR1 (Asset Synthesis):** The `FloodPulseStudio` orchestrator synthesizes mission-specific maps upon persona request using Gemini 2.5/3.5 Flash.
- **FR2 (Telemetry-Aware Synthesis):** The orchestrator pulls real-time environmental telemetry (Weather) and terrain data (Vision) to generate a unified mission risk assessment.
- **FR3 (Artifact Promotion):** Automated pipeline moves validated assets from /level_0/outputs to the public /level_1/assets registry.
- **FR4 (Memory Injection):** Contextual injection of persona metadata (Level 0) into callback_context to ensure agents are "Persona-Aware."
- **FR5 (Interaction):** Interactive discovery phase where the root agent greets the user and determines mission parameters before synthesizing assets.
- **FR6 (Idempotency):** Check-before-create logic ensures cost-efficient Gemini 2.5/3.5 utilization.

### 4.3 Graph Orchestration (Completed)
- **FR7: Persistent State:** The system utilizes **Google Cloud Spanner** (Instance: survivor-network) to store the Trinity (Sarah, Juma, Kamau) as living graph nodes. (✅ Implemented via `spanner_init.py`)
- **FR8: Relational Intelligence:** Implemented `FloodResilienceGraph` with ConnectedTo edges to map emergency lifelines between residents and responders. (✅ Implemented)
- **FR9: Data Integrity:** System supports Idempotent Initialization and "Smart Repair" logic to ensure infrastructure stability in unstable connectivity environments. (✅ Implemented)
- **FR10: GQL-Based Routing:** The system uses **Google Query Language (GQL)** to filter nodes by risk index and return optimized responder paths. (✅ Implemented)

## 5. Technical Validation: "The Mbagathi Truth"
- **Baseline:** Validated spatial reasoning for topographical analysis (**Gemma 4 (31B)** , **Gemini-2.5-Flash**)
- **Graph Verification:** Confirmed directed pathing from Sarah (Resident) at high-risk sump coordinates to Juma (Responder).
- **Data Pivot:** Optimized location data using WKT String format for cross-platform compatibility.

## 6. Non-Functional Requirements (NFR)
- **Latency:** Inference for terrain risk analysis must be < 2 seconds.
- **Pipe Integrity:** Background telemetry redirected to `stderr` to preserve MCP JSON-RPC stream integrity.
- **Credit Awareness:** All LLM calls gated by idempotent checks to minimize API spend.
- **Edge Readiness:** Architecture maintains modularity to support future porting to Android 17 on-device AppFunctions using Gemma 4