# 🌊 Project One-Pager: FloodPulse

Project Lead: Mitchell Odili

Status: In-Development (Hackathon Phase)

Stakeholders: Nairobi Urban Planning, Kenya Red Cross, Google DeepMind (Hackathon)

## 1. The Problem Statement

During the March 2026 rains in Nairobi, flash floods turned arterial roads (like Lang'ata and Mbagathi) into death traps within minutes.
- The Gap: Existing navigation tools (Google Maps/Waze) rely on active internet and crowdsourced data. When the grid fails, the data stops.
- The Impact: Residents lack the "Local Truth" needed to find safe ridges and avoid submerged underpasses, leading to preventable loss of life.

## 2. The Solution: "Nairobi-First" Edge AI

FloodPulse is an offline-first, multimodal resilience assistant. It uses the phone's native hardware to "see" and "reason" about flood risks without needing a cloud connection.
- Vision: To provide every smartphone user in the Global South with a "Digital Guardian" that works when the world goes dark.
- Simulated Validation: We utilize a Modular Agentic Simulation to model the Mbagathi River basin, allowing us to validate "Trinity" persona interactions and multi-agent consensus protocols in high-risk scenarios.
  
## 3. Key User Journeys

- The Stranded Commuter: "My data is down, and I'm at T-Mall. Is the road ahead safe?"
- The Local (Boda) Responder: "I am navigating the Mbagathi backstreets to reach a stranded family. I need to use my camera to 'pulse' the road ahead and verify if the soil is too saturated for my bike."
- The Urban Planner/Strategist: "I need to aggregated 'Ground Truth' data from offline devices to understand where the Mbagathi River actually breached, so we can update the city's drainage priority list."

## 🎮 4. The Development Journey
This project follows a structured, simulation-based progression to move from conceptual identity to a fully orchestrated multi-agent rescue system. Each level builds a critical technical dependency for the next.

| Level | Mission | Technical Dependency | Tech Stack |
|-------|---------|----------------------|------------|
| **Level 0** | **Identity & Baseline** | **Setup:** Establish the "Trinity" of user personas ( Commuter, Responder, Strategist) and the base geospatial asset pipeline. | Multi-Sided Personas, Asset Pipeline, PRD, Multi-turn image generation, Gemini (Nano Banana)|
| **Level 1** | **Terrain Pinpointing** | Discovery: Zero-shot vision analysis using Gemma 4 to identify static "Sumps" vs "Ridges" in the Mbagathi corridor. | Gemma 4 31B, Spatial Vision Analysis |
| **Level 2** | **Event-Driven SOS** | Ingest: Capturing live telemetry (SOS "Pulses") from Stranded Commuters to create dynamic nodes in the environment. | Event-driven agents, A2A communication |
| **Level 3** | **Graph Orchestration** | **Compute:** Matching Responders to Commuters via pathfinding logic across dynamic nodes to find real-time safe routes. | Cloud Spanner Graph (GQL), Pathfinding |
| **Level 4** | Coordinate group rescue | **Orchestration:** Multi-agent coordination to prevent traffic bottlenecks on "Safe Ridges" during mass evacuation events. | Agent orchestration, logistics, consensus protocols |

---

## 🧪 5. Phase 1: Technical Feasibility (Mbagathi Basin)
To validate the **FloodPulse** core reasoning, we conducted a zero-shot analysis using **Gemma 4 (31B)** on high-resolution satellite imagery of the Mbagathi River corridor.

### **Key Findings:**
* **River Path:** Successfully identified the riparian corridor despite urban canopy cover.
* **Critical Nodes:** Pinpointed three high-risk intersections:
    1. **Lang'ata Road/ICC Crossing:** Identified as a primary arterial bottleneck.
    2. **South B/C Border:** Identified as a "low-water" neighborhood split-point.
    3. **Lower Basin Sumps:** Corrected identified as high-risk vehicle entrapment zones.
* **Safe Ridge Logic:** The model autonomously identified the **South B Plateau** as a primary evacuation zone based on spectral terrain analysis (elevation vs. drainage).

> **Status:** ✅ Feasibility Confirmed. The model demonstrates the required spatial intuition for urban flood navigation.

---

## 🛠️ 6. Technical Stack: The Path to Production
We leverage a hybrid stack that moves from rapid AI prototyping to high-scale cloud infrastructure.

| Environment | Purpose | Core Technologies |
|-------------|---------|-------------------|
| **AI Studio** | **Prototyping** | Gemma 4 31B (Multimodal Reasoning) |
| **Kaggle** | **Data Engineering** | Geospatial Notebooks, NASA SRTM Datasets | 
| **GitHub** | **Source & CI/CD** | Python, Model Context Protocol (MCP) |
| **Google Cloud** | **Production Scale** | Cloud Spanner (Graph), FastAPI, Cloud Run |

---

## 🛰️ 7. Technical Deep Dive: The "Hidden River" Problem

Standard navigation apps often fail in Nairobi because the Mbagathi River is obscured by urban canopy and informal settlements. **FloodPulse** solves this through a "Multi-Sensor Fusion" approach:

### **a. Multimodal Spatial Reasoning**
We leverage **Gemma 4** to analyze soil moisture levels (spectral darks) and vegetation density. The AI "sees" the river's true path even when it's missing from official map layers.

### **b. NASA SRTM Integration**
We cross-reference AI visual findings with **NASA Shuttle Radar Topography Mission (SRTM)** data. This ensures that every "Safe Ridge" suggested by the app is mathematically validated for elevation—not just a visual guess.

### **c. SAR (Synthetic Aperture Radar) Capability**
Optical satellites can't see through Nairobi's storm clouds. Our roadmap includes integrating **Sentinel-1 SAR** data, which uses radar to detect standing water through cloud cover, providing a "Pulse" of the flood in real-time.

---
  
## 8. Success Metric

- Inference Speed: < 2 seconds for local image-to-risk analysis.
- Offline Parity: 100% of core safety features must work in Airplane Mode.
- Validation: 90% alignment between AI-predicted flood zones and UNOSAT post-disaster maps.
