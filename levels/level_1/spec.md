# Level 1: The Studio Architecture Specification

## 1. Overview
The **Studio** is the core Agentic Synthesis engine for the FloodPulse Nairobi project. It moves beyond linear script execution to a persistent, goal-oriented pipeline that leverages the **Google Agent Development Kit (ADK)** to orchestrate specialized agents. This system synthesizes mission-critical data in real-time for the Mbagathi Basin, maintaining state-aware context throughout the life of a mission.

## 2. Agentic Roles (Hierarchy)
- **Orchestrator (The Director):** The Root Agent implemented as a `SequentialAgent`. It manages mission requests, performs task delegation via a predefined workflow, and synthesizes final outputs.
- **Weather Agent:** A specialized sub-agent for fetching and interpreting live environmental telemetry (OpenWeather API).
- **Vision Agent:** A specialized sub-agent for topographical/terrain risk assessment utilizing spatial reasoning and vision-based tool calling.

## 3. Orchestration Workflow
The Studio utilizes the ADK’s sequential execution pattern to adhere to the "Resilience Protocol":
1. **Delegation:** The Director receives user intent and maps it to a sequential flow.
2. **Sequential Flow:**
- **Step 1:** Telemetry Fetching (WeatherGatherer gathers real-time data).
- **Step 2:** Terrain Assessment (VisionAnalyst evaluates spatial hazards).
- **Step 3:** Visualization (Mapping tool overlays safety status).
3. **Session Management:** All transitions are handled within an `InMemorySessionService` registry, ensuring the conversation context is maintained throughout the sequential delegation.

## 4. Tool Registry (The "Hands")
- `generate_mission_map(responder_name, lat, lon)`: Draws responder identities onto the static basemap with color-coded risk status.
- `get_nairobi_pulse_tool(lat, lon)`: Extracts rainfall and intensity data to inform the Studio’s risk assessment.
- `analyze_terrain_risk(lat, lon)`: Maps coordinates to known hazard nodes (sumps, arterial bottlenecks) via the internal graph reference.

## 5. State Management & Idempotency
- **Registry:** ADK-managed Session objects for high-concurrency, memory-resident state tracking.
- **Idempotency:** The Runner handles task execution logic. By tracking invocation_ids, the system ensures that complex tool-calling chains are atomic and traceable.
- **Resilience:** The system utilizes tenacity for automatic retry strategies during transient API unavailability (e.g., 503 errors).

## 6. Interaction Loop
1. **Trigger:** `main.py` initializes the `Runner` and registers a `session_id` within the `InMemorySessionService`.
2. **Perception:** The Director invokes the `SequentialAgent` logic to trigger sub-agents..
3. **Reasoning:** Sub-agents execute tools sequentially, passing results back up to the Director.
4. **Action:** The Vision/Mapping agents render the status update.
5. **Report:** The Director returns a final `Content` object summarizing the terrain status and mission outcomes.

---

### Workflow Visualization
![FloodPulse Studio Workflow](../../docs/level_1_workflow_viz.png)