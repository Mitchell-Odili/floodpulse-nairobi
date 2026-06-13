# Level 1: The Studio Architecture Specification

## 1. Overview
The **Studio** is the core Agentic Synthesis engine for the FloodPulse Nairobi project. It moves beyond linear script execution to a persistent, goal-oriented pipeline that leverages the **Google Agent Development Kit (ADK)** to orchestrate specialized agents. This system synthesizes mission-critical data in real-time for the Mbagathi Basin, maintaining state-aware context throughout the life of a mission.

## 2. Agentic Roles (Hierarchy)
- **Orchestrator (The Director):** The Root Agent implemented as a `SequentialAgent`. It is responsible for validating and persisting user-provided mission context (Name, Lat, Lon) into the `session.state` via the Context Setter tool before delegating domain tasks.
- **Weather Agent:** A specialized sub-agent for fetching and interpreting live environmental telemetry (OpenWeather API).
- **Vision Agent:** A specialized sub-agent for topographical/terrain risk assessment utilizing spatial reasoning and vision-based tool calling.

## 3. Orchestration Workflow
The Studio utilizes the ADK’s sequential execution pattern to adhere to the "Resilience Protocol":
1. **Context Initialization:** The Director captures mission details and calls the `update_mission_context` tool to initialize the session.state. Execution is blocked until this context is verified.
2. **Delegation:** The Director maps the verified context to the sequential flow.
3. **Sequential Flow:**
- **Step 1:** Telemetry Fetching (WeatherGatherer gathers real-time data).
- **Step 2:** Terrain Assessment (VisionAnalyst evaluates spatial hazards).
- **Step 3:** Visualization (Mapping tool overlays safety status).
4. **Session Management:** All transitions are handled within an `InMemorySessionService` registry, ensuring the conversation context is maintained throughout the sequential delegation.

## 4. Tool Registry (The "Hands")
- `update_mission_context(responder_name, lat, lon)`: Persists raw user input into the `tool_context.session.state`. This tool acts as the "Gatekeeper," ensuring downstream agents have access to standardized mission parameters.
- `generate_mission_map(responder_name, lat, lon)`: Draws responder identities onto the static basemap with color-coded risk status.
- `get_nairobi_pulse_tool(lat, lon)`: Extracts rainfall and intensity data to inform the Studio’s risk assessment.
- `analyze_terrain_risk(lat, lon)`: Maps coordinates to known hazard nodes (sumps, arterial bottlenecks) via the internal graph reference.

## 5. State Management & Idempotency
- **Context Injection:** State is explicitly injected via `tool_context.session.state`, ensuring that `weather_tools` and `map_tools` receive validated parameters.
- **Resilience Layer:** Integrated `@genai/http_retry` (exponential backoff with jitter) handles transient `429` (Quota) and `503` (Unavailable) errors, ensuring mission continuity despite external API limitations.
- **Asset Caching:** Idempotent file management ensures that if a mission map or tile already exists on the disk, the system bypasses external API calls, reducing latency and protecting daily rate limits.

## 6. Interaction Loop
1. **Trigger:** `main.py` initializes the `Runner` and registers a `session_id` within the `InMemorySessionService`.
2. **Perception:** The Director invokes the `SequentialAgent` logic to trigger sub-agents..
3. **Reasoning:** Sub-agents execute tools sequentially, passing results back up to the Director.
4. **Action:** The Vision/Mapping agents render the status update.
5. **Report:** The Director returns a final `Content` object summarizing the terrain status and mission outcomes.

**Protocol Note:** If the `session.state` is found to be missing required latitude or longitude during tool invocation, agents must trigger a `ValueError`, forcing the Director to re-engage the user for missing mission parameters.

---

### Workflow Visualization
![FloodPulse Studio Workflow](../../docs/level_1_workflow_viz.png)