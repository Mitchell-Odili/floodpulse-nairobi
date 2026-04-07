# 🌊 FloodPulse: Nairobi-First Edge AI

**Offline-First Multi-Agent Resilience for the Mbagathi Basin**

Project Lead: Mitchell Odili

**Status:** Status: ✅ Level 1 Complete | 🌊 Level 2 Integration Starting

**Mission:** Validating "Digital Guardian" protocols for urban flood resilience using multimodal LLMs and geospatial agent orchestration.

---

## 🚨 1. The Problem: The "Data Darkness" Gap

During the March 2026 rains in Nairobi, flash floods turned arterial roads (like Lang'ata and Mbagathi) into death traps within minutes.
- The Gap: Existing navigation tools (Google Maps/Waze) rely on active internet and crowdsourced data. When the grid fails, the data stops.
- The Impact: Residents lack the "Local Truth" needed to find safe ridges and avoid submerged underpasses, leading to preventable loss of life.
- The Reality: In a crisis, the map is often the first thing to go dark. 

## 🛡️ 2. The Solution: Multimodal Edge Resilience

FloodPulse is an offline-first, multimodal resilience assistant. It uses the phone's native hardware to "see" and "reason" about flood risks without needing a cloud connection.
- Vision: A "Digital Guardian" for the Global South that works when the world goes dark.
- Validation: A Modular Agentic Simulation modeling the Mbagathi River basin to validate multi-agent consensus in high-risk scenarios.

---

## 🧪 3. Technical Feasibility (Mbagathi Basin)
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
  
## 🧬 4. Level 0: Identity Orchestration (The Trinity)

To simulate Nairobi's flood dynamics, we've architected a **Parametric Persona Engine.** This ensures that our agents—the Stranded Commuter, the Local/Boda Responder, and the Urban Strategist—have consistent identities.

**Technical Implementation:**
- Orchestrator (`create_identity.py`): The "Brain." Manages batch generation, directory routing, and **Credit Saver** logic for cost-efficient, idempotent runs.

- Worker (`generator.py`): The "Muscle." Leverages **Gemini 2.5 Flash** chat sessions to maintain **Visual Identity Consistency** (e.g., ensuring a specific Kenyan flag beaded bracelet carries from portraits to map icons).

- Asset Pipeline: Automated promotion of AI outputs to production directories: `/assets/avatars/` and `/assets/maps/`.

---

## 🎮 5. The Development Journey
This project follows a structured, simulation-based progression to move from conceptual identity to a fully orchestrated multi-agent rescue system. Each level builds a critical technical dependency for the next.

| Level | Mission | Technical Dependency | Tech Stack |
|-------|---------|----------------------|------------|
| **Level 0** | **Identity & Baseline** | **Orchestration:** Established the "Trinity" of user personas ( Commuter, Responder, Strategist) and the base geospatial asset pipeline. | Orchestrator/Worker Pattern, Vertex AI, Gemini 2.5 Flash, PIL |
| **Level 1** | **Terrain Pinpointing** | **Infrastructure:** Implemented Model Context Protocol (MCP) for real-time vision analysis of the Mbagathi basin. | **MCP**, Gemini 2.5 Flash, Google Static Maps |
| **Level 2** | **The Pulse (SOS)** | **Ingest:** Capturing live telemetry (SOS "Pulses") and OpenWeather data to create dynamic environment risk. | Event-driven agents, OpenWeather API, A2A communication |
| **Level 3** | **Graph Orchestration** | **Compute:** Matching Responders to Commuters via pathfinding logic across dynamic nodes to find real-time safe routes. | Cloud Spanner Graph (GQL), Pathfinding |
| **Level 4** | **Coordinate group rescue** | **Orchestration:** Multi-agent coordination to prevent traffic bottlenecks on "Safe Ridges" during mass evacuation events. | Agent orchestration, consensus protocols |

---

## 🛠️ 6. Technical Stack: The Path to Production
We leverage a hybrid stack that moves from rapid AI prototyping to high-scale cloud infrastructure.

| Environment | Purpose | Core Technologies |
|-------------|---------|-------------------|
| **AI Studio** | **Prototyping** | Gemma 4 31B (Multimodal Reasoning) |
| **Vertex AI** | **Orchestration** | Gemini 2.5 Flash (Multimodal Persona Consistency) |
| **Kaggle** | **Data Engineering** | Geospatial Notebooks, NASA SRTM Datasets | 
| **GitHub** | **Source & CI/CD** | Python, Model Context Protocol (MCP) and FastMCP |
| **Google Cloud** | **Production Scale** | Cloud Spanner (Graph), FastAPI, Cloud Run |

---

## 🛰️ 7. Technical Deep Dive: The "Hidden River" Problem

Standard maps often fail in Nairobi because the Mbagathi River is obscured by urban canopy and informal settlements. **FloodPulse** solves this through a "Multi-Sensor Fusion" approach:

- **Multimodal Spatial Reasoning:** AI analyzes soil moisture (spectral darks) to "see" the true path.
- **Multi-Sector Tactical Spread:** Automated generation of Zoom-17 mission tiles for distinct topographical zones (Sump, Arterial, Ridge) to ensure high-definition context for local AI reasoning.
- **NASA SRTM Integration:** Mathematical validation of elevation for every "Safe Ridge."
- **SAR (Synthetic Aperture Radar) Capability:** Integrating Sentinel-1 SAR to detect standing water through cloud cover in real-time.

---
  
## 🎯 8. Success Metric

- Inference Speed: < 2 seconds for local image-to-risk analysis.
- Offline Parity: 100% of core safety features must work in Airplane Mode.
- Validation: 90% alignment between AI-predicted flood zones and UNOSAT post-disaster maps.

## 📍 9. Initial Deployment Nodes

| Agent | Landmark | Coordinates | Risk profile |
|-------|----------|-------------|------|
| **Sarah - Stranded Commuter** | T-Mall Underpass | `-1.3148, 36.8115` | Hydrological Low Point |
| **Juma - Local/Boda Responder** | Lang'ata Arterial | `-1.3165, 36.8135` | Infrastructure Bottleneck | 
| **Kamau - Urban Strategist** | Madaraka Ridge | `-1.3110, 36.8185` | Strategic High Ground | 