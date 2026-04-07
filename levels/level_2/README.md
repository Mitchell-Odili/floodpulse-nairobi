## 🌧️ Level 2: The Mbagathi Pulse (Weather Telemetry)

**Mission Overview**
Level 2 moves FloodPulse from "Static Maps" to "Dynamic Environment." We transition the Digital Guardian from just seeing the ground to "feeling" the sky by integrating real-time hydrological data.

**Core Objectives**
- **Environmental Telemetry:** Integrating the OpenWeather API to fetch real-time precipitation data for the Mbagathi corridor.
- **Data Normalization:** Translating raw rainfall (mm/h) into a standardized **Flash Index (0.0 - 1.0)**.
- **Multi-Sensor Fusion:** Upgrading the MCP protocol to inject live weather data into the Vision AI's reasoning loop.

---

**🛠️ Technical Components**
1. `weather_service.py`
- **Logic:** Implemented a robust API fetcher with **Standard Error (stderr) Logging** to ensure MCP pipe integrity.
- **Normalization:** Uses a 50mm/h normalization threshold to calibrate the Flash Index for Nairobi's "Long Rains."

2. `vision_mcp.py` (Upgraded from Level 1)
- **SDK:** Migrated to the modern `google-genai` SDK for Gemini 2.5 Flash.
- **Fusion:** Merged `get_nairobi_pulse` logic into the `analyze_mbagathi_risk` tool.

---

**🛰️ The Flash Index (0.0 - 1.0)**
| Index Range | Status | AI Directive |
|-------------|--------|--------------|
| **0.0 - 0.2** | 🟢 Low Pulse | Monitor and stay put. |
| **0.3 - 0.6** | 🟡 Moderate Pulse | Avoid Sumps (T-Mall). Prepare for runoff. |
| **0.7 - 1.0** | 🔴 Critical Pulse | IMMEDIATE EVACUATION to the Ridge. |