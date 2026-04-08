# 📄 Product Requirements Document: FloodPulse (Nairobi)
**Project Code:** FP-NBO-2026

**Status:** Status: 🟢 Completed (Level 3) | 🟡 Level 4 Pending.

## 1. Problem Statement
Existing navigation tools in Nairobi rely on static road data and active internet. During flash floods in the Mbagathi basin, infrastructure fails rapidly. Users lack a real-time, offline-first tool to identify "Ground Truth" hazards and find high-ground ridges.

## 2. Goals & Objectives
- **Goal:** Reduce transit-related flood fatalities by 50% in pilot areas.
- **Objective:** Deploy an edge-AI model (Gemma 4) capable of identifying flood boundaries without a data connection.
- **Strategic Metric:** Achieve < 2-second local inference for topographical risk analysis.

## 3. System Architecture
To achieve "Offline-First" resilience, the system follows a Modular Agentic Simulation pattern:

- **Orchestration Engine:** A Python-based "Brain" managing the **"Trinity"** of user personas.
- **The Trinity Engine (Level 0):** Uses **Gemini 2.5 Flash** for high-fidelity identity and asset generation (Kenya-specific cultural markers).
- **Geospatial Layer (Level 1):** Uses **Google Static Maps API** to fetch 640x640 satellite tiles for local caching (Mbagathi Sump, Langata Arterial, South B Ridge).
- **Environmental Pulse (Level 2):** Integrates real-time precipitation telemetry via **OpenWeather API**. It converts raw meteorological data into a standardized Flash Index (0.0 - 1.0) to trigger autonomous safety protocols.
- **Graph Orchestration (Level 3):** A persistent **Google Cloud Spanner** backbone that maps the "Trinity" as living nodes. It calculates dynamic "Safe Edges" (navigable paths) by cross-referencing terrain sumps with real-time weather intensity.

### 3.1 Modular Evolution Matrix
| Feature | Level 1: Terrain (Vision) | Level 2: Pulse (Telemetry) | Level 3: Graph (Orchestration) |
|-------------|--------|--------------|---------------|
| **Status** | ✅ Completed| ✅ Completed | ✅ Completed |
| **Primary Data** | Google Static Maps API | OpenWeather API | Google Cloud Spanner |
| **Core Logic** | Multi-Sector Pixel Analysis | Flash Index Normalization | Property Graph Traversal (GQL) |
| **AI Mandate** | Identification (Sump vs Ridge) | Risk Assessment (Critical Alert) | Networked Resilience (SOS) |

### 3.2 Architectural Resilience: Dual-Redundancy DDL
To ensure "offline-first" reliability and prevent deployment failures in low-connectivity environments, the Spanner initialization layer utilizes a **Dual-Redundancy DDL pattern.**

- **Primary:** The system attempts to fetch the schema from a local `schema.sql` file.
- **Secondary (Fail-Safe):** In the event of file-path corruption or missing artifacts, the system falls back to an **Internal Hardcoded DDL** manifest to ensure the database "Brain" can always be reconstituted

## 4. Technical Specifications & Progress
### 4.1 Identity Orchestration (Completed)
- **Logic:** Implemented `create_identity.py` and `generator.py` using an Orchestrator/Worker pattern.
- **Output:** Generated consistent visual assets stored in `level_0/assets/.`

### 4.2 Terrain Pinpointing (Completed)
- **FR1:** The system MUST cache high-resolution (Zoom 17) satellite tiles locally to support offline navigation. (✅ Implemented via `static_mapper.py`)
- **FR2:** The system MUST overlay agent positions onto satellite terrain with sub-meter precision using unique mission-sector tiles. (✅ Implemented)
- **FR3:** The system MUST utilize Model Context Protocol (MCP) to bridge local image data with Multimodal LLMs (Gemini 2.5 Flash). (✅ Implemented via `vision_mcp.py`)
- **FR4:** The system MUST support Multi-Sector Perception, allowing unique risk assessments for different topographical zones (Sump, Arterial, Ridge). (✅ Implemented)

### 4.3 Dynamic Environment (Completed)
- **FR5: Enviromental Telemetry:** The system fetches real-time rainfall data from the OpenWeatherMap API for the Mbagathi corridor. (✅ Implemented via `weather_service.py`).
- **FR6: The Flash Index:** Implemented a normalization logic (0.0 - 1.0) that calculates risk based on 50mm/h rainfall thresholds. (✅ Implemented)
- **FR7: Multi-Sensor Fusion** The MCP server (`vision_mcp.py`) now fuses Level 1 Terrain pixels with Level 2 Weather Pulse to generate high-fidelity safety directives. (✅ Implemented)

### 4.4 Graph Orchestration (Level 3 - In Progress)
- **FR8: Persistent State:** The system utilizes **Google Cloud Spanner** (Instance: survivor-network) to store the Trinity (Sarah, Juma, Kamau) as living graph nodes. (✅ Implemented via `spanner_init.py`)
- **FR9: Relational Intelligence:** Implemented `FloodResilienceGraph` with ConnectedTo edges to map emergency lifelines between residents and responders. (✅ Implemented)
- **FR10: Data Integrity:** System supports Idempotent Initialization and "Smart Repair" logic to ensure infrastructure stability in unstable connectivity environments. (✅ Implemented)
- **FR11: GQL-Based Routing:** The system uses **Google Query Language (GQL)** to filter nodes by risk index and return optimized responder paths. (✅ Implemented)

## 5. Technical Validation: "The Mbagathi Truth"
- **Baseline:** Validated **Gemma 4 (31B)** spatial reasoning.
- **Graph Verification:** Confirmed directed pathing from Sarah (Resident) at high-risk sump coordinates to Juma (Responder).
- **Data Pivot:** Successfully transitioned from `ST_GEOMETRY` to **WKT String** format for location data to ensure cross-region compatibility without sacrificing spatial accuracy.

## 6. Non-Functional Requirements (NFR)
- **Offline Latency:** Inference for terrain risk analysis must be < 2 seconds.
- **Flash Index Latency:** API fetch and normalization must occur in < 1.5 seconds to ensure the Pulse remains "Real-Time."
- **Pipe Integrity:** All background telemetry MUST be redirected to stderr to prevent JSON-RPC corruption in the MCP stream.
- **Data Sovereignty:** Mission-critical API keys MUST be stored in .env and excluded from source control.
- **Interoperability:** System architecture must support NASA SRTM and Sentinel-1 SAR data feeds.