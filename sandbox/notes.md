# 📝 MCP & Configuration Lab Notes

## 1. The Model Context Protocol (MCP)
MCP is the bridge that transforms static environmental data into Actionable Intelligence. It serves as our core engine for agentic tools.

### Strategic Functions
- **The "Eyes" (Multimodal Perception):** Allows models like Gemini to directly analyze local files (e.g., `mbagathi_basemap.png`) to identify spectral indicators of standing water.
- **The "Brain" (Spatial Reasoning):** Enables agents to cross-reference coordinates with Digital Elevation Models (DEMs) to provide precise evacuation logic (e.g., "Sarah is in a 4-meter depression; move North-East").
- **The "Guardian" (Offline-First Logic):** Allows agents to use specialized local tools (Python scripts for slope/elevation) without relying on fragile cloud APIs.

## 2. Technical Implementation
### Tooling Strategy
- **FastMCP:** High-level framework for building MCP servers.
- **Testing with Inspector:**
```
1. Install: npm install -g @modelcontextprotocol/inspector
2. Launch: npx @modelcontextprotocol/inspector uv run sandbox/vision_mcp.py
3. Access dashboard via http://localhost:6274 to interact with tools.
```

## 3. Authentication & Access Strategy
We have unified our MCP servers into a single `vision_mcp.py` file, utilizing a `.env` toggle (`USE_VERTEX_AI=true/false`) to switch between rapid-iteration and production-grade authentication.

| Feature | API Key Mode | ADC Mode - Vertex AI |
|-------------|--------|--------------|
| **Primary Use** | Rapid Prototyping | Production/Studio Deployment |
| **Authentication** | Direct `GOOGLE_API_KEY` | Managed via `gcloud` identity |
| **Quota** | Account-level limits | Project-level (IAM) quotas |
| **Best For** | Bypassing IAM bottlenecks | Secure enterprise integration |

### Performance Insights: The "Hanging" Latency
- **Secure Tunneling:** Requests are routed through GCP infrastructure for permission validation.
- **Multimodal Inference:** Overhead for processing image bytes alongside text.
- **Cold Start:** The initial handshake to spin up the model instance and verify identity.

## 4. Operational Logs & Errors
- Model Availability:
- **Gemini 3.5-Flash:** Currently restricted in our Google Cloud ADC environment.
- **Gemini 2.5-Flash:** Used as the stable baseline for all MCP spatial reasoning tasks within the current production pipeline.
- **Configuration:** The project now utilizes a hierarchical path resolution that allows the `vision_mcp` script to operate as a post-execution auditor; in this architecture, Level 1 establishes the Mission Baseline, while the Vision MCP performs independent Post-Mission Verification to ensure rigorous quality control.

## 🛠️ Inspector Deployment Note
- **Observed Limitation:** The MCP Inspector struggles to maintain stable connections when launched within a remote cloud development environment (like Cloud Shell) due to network tunneling restrictions.
- **Workaround:** Inspector performs optimally when executed in a **local VS Code terminal.** Ensure your local development machine has the required Python environment and npm installed to maintain visibility into the MCP server’s tool-calling logic.
- **Validation:** All successful verification screenshots in this repository were captured from a local development environment.

## 🧪 Inspector Results Evidence
![analyze_mbagathi_risk output](../docs/mcp_inspector_test.png)