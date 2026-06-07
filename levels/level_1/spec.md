# Level 1: The Studio Architecture Specification

## 1. Overview
The **Studio** is the core Agentic Synthesis engine for the FloodPulse Nairobi project. It moves beyond linear script execution to a persistent, goal-oriented pipeline that orchestrates specialized agents to synthesize mission-critical data in real-time for the Mbagathi Basin.

## 2. Agentic Roles (Hierarchy)
- **Orchestrator (The Director):** The Root Agent. It manages mission requests, performs task delegation, and synthesizes final outputs. It maintains the "Studio" state and enforces persona-aware context.
- **Weather Agent:** A specialized sub-agent for fetching and interpreting live environmental telemetry (OpenWeather API).
- **Vision Agent:** A specialized sub-agent for topographical/terrain risk assessment using spatial reasoning.

## 3. Orchestration Workflow
The Studio utilizes three primary workflow patterns to execute its mission:
- **Sequential:** Follows the "Resilience Protocol": (1) Fetch Telemetry $\rightarrow$ (2) Assess Terrain $\rightarrow$ (3) Visualize Risk.
- **Parallel:** Triggers simultaneous data gathering across multiple Mbagathi nodes to reduce latency during emergency discovery.
- **Loop:** Enables continuous monitoring of critical sumps and low-water split points until safety thresholds are restored.

## 4. Tool Registry (The "Hands")
- `update_map(avatar_name, x, y, status)`: Draws responder identities onto the static basemap with color-coded risk status (Red/Green).
- `get_weather_data(lat, lon)`: Extracts rainfall and intensity data to inform the Studio’s risk assessment.
- `analyze_terrain_risk(lat, lon)`: Maps coordinates to known hazard nodes (sumps, arterial bottlenecks) via the internal graph reference.

## 5. State Management & Idempotency
- **Registry:** All agentic states and responder positions are tracked in `data/registry.json`.
- **Idempotency:** Before any tool execution (e.g., generating a mission map), the Orchestrator checks the registry to ensure the task hasn't already been completed for the current environment state, minimizing unnecessary API calls.

## 6. Interaction Loop
1. **Trigger:** A telemetry event or user request initiates the Studio.
2. **Perception:** The Director triggers sub-agents to gather data.
3. **Reasoning:** The Studio synthesizes data (Weather + Terrain) into a JSON safety assessment.
4. **Action:** The map tool overlays the avatar with the final safety status.
5. **Report:** The Studio provides a natural language summary of the risk to the user.

---

### Workflow Visualization
![FloodPulse Studio Workflow](../../docs/level_1_workflow_viz.png)