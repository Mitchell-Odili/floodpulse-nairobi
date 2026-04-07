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
- **Logic:** Implemented a **Multi-Sector Perception** loop. Instead of a single map, it fetches unique Zoom 17 satellite tiles for each agent to provide maximum visual context for the AI.
- **Optimization:** Uses `.copy()` logic for memory efficiency and ensures Idempotency in asset generation.

2. `vision_mcp.py` 
- **Protocol:** A production-grade **Model Context Protocol** server.
- **Intelligence:** Integrated with Gemini 2.5 Flash (via the modern `google-genai` SDK) to perform real-time pixel analysis.
- **Functionality:** Exposes the `analyze_mbagathi_risk` tool, which performs **Multi-Sensor Fusion**. It cross-references static **Terrain Mapping** (identifying riparian sumps/ridges) with **Live Weather Telemetry** (Flash Index 0.0-1.0) to provide real-time, high-fidelity safety directives for the Mbagathi Basin.

---

**📍 Initial Deployment Nodes**

| Agent | Landmark | Coordinates | Role |
|-------|----------|-------------|------|
| **Sarah** | T-Mall Underpass | `-1.3148, 36.8115` | The "Sump" Observer |
| **Juma** | Lang'ata/ICC | `-1.3165, 36.8135` | The Arterial Responder | 
| **Kamau** | Madaraka/Highview | `-1.3110, 36.8185` | The Ridge Strategist | 