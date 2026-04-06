## 🛰️ Level 1: Terrain Discovery & Pinpointing
**Mission Overview**
Level 1 transitions FloodPulse from persona archetypes to geospatial reality. Using the "Trinity" identities established in Level 0, we perform zero-shot visual analysis of the **Mbagathi River Basin** to identify critical flood sumps and safe ridges.

**Core Objectives**
- **Geospatial Anchoring:** Fetching high-resolution satellite imagery via Google Static Maps API.
- **Multi-Agent Visualization:** Dynamically overlaying agent sprites onto real-world coordinates (T-Mall, Lang'ata Road).
- **Offline-First Strategy:** Implementing local image caching to ensure the "Digital Guardian" remains functional during infrastructure blackouts.

---

**🛠️ Technical Components**
1. `static_mapper.py`
The primary worker for this level. It handles the coordinate-to-pixel translation and "blits" agent icons onto the satellite base layer.

- **Input:** Latitude/Longitude coordinates + Level 0 Assets.
- **Output:** sarah_on_mission.png (Visual mission brief).

2. `map_discovery.py` (In-Development)
The orchestrator that will manage the transition from static coordinates to dynamic event-driven "Pulses."

3. `vision_mcp.py` (Planned)
A Model Context Protocol (MCP) server that will allow LLMs (Gemma 4 / Gemini 2.5) to "reason" about the topography in the captured images—identifying riparian boundaries and elevation plateaus.

---

**📍 Initial Deployment Nodes**

| Agent | Landmark | Coordinates | Role |
|-------|----------|-------------|------|
| **Sarah** | T-Mall Underpass | `-1.3148, 36.8115` | The "Sump" Observer |
| **Juma** | Lang'ata/ICC | `-1.3255, 36.8020` | The Arterial Responder | 
| **Kamau** | South B Plateau | `-1.3100, 36.8350` | The Ridge Strategist | 