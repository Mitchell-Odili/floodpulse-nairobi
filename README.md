## 🌊 Project One-Pager: FloodPulse

Project Lead: Mitchell Odili

Status: In-Development (Hackathon Phase)

Stakeholders: Nairobi Urban Planning, Kenya Red Cross, Google DeepMind (Hackathon)

**1. The Problem Statement**

During the March 2026 rains in Nairobi, flash floods turned arterial roads (like Lang'ata and Mbagathi) into death traps within minutes.
- The Gap: Existing navigation tools (Google Maps/Waze) rely on active internet and crowdsourced data. When the grid fails, the data stops.
- The Impact: Residents lack the "Local Truth" needed to find safe ridges and avoid submerged underpasses, leading to preventable loss of life.

**2. The Solution: "Nairobi-First" Edge AI**

FloodPulse is an offline-first, multimodal resilience assistant. It uses the phone's native hardware to "see" and "reason" about flood risks without needing a cloud connection.
- Vision: To provide every smartphone user in the Global South with a "Digital Guardian" that works when the world goes dark.
- Pilot: Validating on the Mbagathi River basin due to its high-risk "bowl" topography and accessible ground truth.
  
**3. Key User Journeys**

- The Stranded Commuter: "My data is down, and I'm at T-Mall. Is the road ahead safe?"
- The Local Responder: "I need to map the new river boundary using only my phone camera to update the neighborhood graph."
  
**4. Technical Moat (The "Google" Stack)**
- Intelligence: Gemma 4 E2B (Edge-optimized) for local multimodal reasoning.
- Connectivity: Model Context Protocol (MCP) to bridge the model with pre-cached NASA/Sentinel-1 satellite tiles.
- Navigation: Cloud Spanner Graph logic to calculate the shortest path to "High Ground" nodes during a breach.
  
**5. Success Metrics**

- Inference Speed: < 2 seconds for local image-to-risk analysis.
- Offline Parity: 100% of core safety features must work in Airplane Mode.
- Validation: 90% alignment between AI-predicted flood zones and UNOSAT post-disaster maps.

