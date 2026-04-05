## 🎮 Level 0: Explorer Identity & Baseline

**🛰️ Mission Objective**

Establish the foundational "User Personas" and technical environment for the FloodPulse ecosystem. This level focuses on identity generation and the geospatial asset pipeline required for the Mbagathi Basin pilot.

**👥 The Trinity Personas**

In this level, the user selects one of three distinct identities. Each identity validates a different layer of the technical stack:

1. The Stranded Commuter: Validates Event-Driven SOS (Level 2) and high-stress UI simplicity.
2. The Local/Boda-Responder: Validates Gemma 4 31B on-device vision and offline navigation.
3. The Urban Strategist: Validates Cloud Spanner Graph GQL queries and Multi-Agent Orchestration.

**🧬 Persona Logic & Asset Pipeline**

The Nairobi Trinity (Sarah, Juma, and Kamau) is generated using a Parametric Orchestration model. Instead of manual creation, the system uses a shared configuration to ensure visual consistency across different perspectives.

- Identity Consistency: Uses Gemini 2.5 Flash Image chat sessions to carry visual traits (e.g., the Kenyan flag beaded bracelet) from the 2D portrait to the top-down map icon.

- Asset Management: A modular pipeline separates "Drafts" (temporary outputs) from "Production Assets." Finalized sprites are promoted to categorized directories in /assets/ for Frontend consumption.

**🛠️ Technical Stack (Level 0)**

| Component | File | Description |
|-------------|---------|-------------------|
| **User Interface** | `customize.py` | UI for selecting the active persona and setting mission metadata. |
| **Orchestrator** | `create_identity.py` | Manages the "Trinity" loop, file pathing, and Credit Saver logic. | 
| **Worker Engine** | `generator.py` | Executes multimodal Vertex AI calls and handles image extraction. |
| **Asset Library** | `/assets/` | Production-ready storage for `avatars/` and `maps/` sprites. |


✅ Success Criteria
- Three distinct user personas defined with specific technical dependencies.
- Base geospatial assets (Mbagathi Satellite Crops) integrated into the project.

**🏃 Next Steps**
Once your identity is established, proceed to Level 1: Terrain Pinpointing to begin the zero-shot spatial analysis of the Mbagathi basin.
