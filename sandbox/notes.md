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
We maintain two distinct paths for MCP experimentation to balance security with development flexibility. 
	

| Feature | Legacy API Key | Application Default Credentials (ADC) - Cloud |
|-------------|--------|--------------|
| **Primary Use** | Prototyping & Paid-tier access| Enterprise-grade production |
| **Model Access** | Full access (including 3.5-Flash) | Restricted to project-level quota |
| **Security** | Sensitive .env management | Secure, time-bound tokens |
| **Environment** | Best for local quick-testing | Best for robust cloud integration |

### Performance Insights: The "Hanging" Latency
- **Secure Tunneling:** Requests are routed through GCP infrastructure for permission validation.
- **Multimodal Inference:** Overhead for processing image bytes alongside text.
- **Cold Start:** The initial handshake to spin up the model instance and verify identity.

## 4. Operational Logs & Errors
- Model Availability:
- **Gemini 3.5-Flash:** Currently restricted in our Google Cloud ADC environment.
- **Gemini 2.5-Flash:** Used as the stable baseline for all MCP spatial reasoning tasks within the current production pipeline.
- **Config Logic:** `config.json` is anchored to the `PROJECT_ROOT` to ensure consistent pathing regardless of the execution directory.

## 🛠️ Inspector Deployment Note
- **Observed Limitation:** The MCP Inspector struggles to maintain stable connections when launched within a remote cloud development environment (like Cloud Shell) due to network tunneling restrictions.
- **Workaround:** Inspector performs optimally when executed in a **local VS Code terminal.** Ensure your local development machine has the required Python environment and npm installed to maintain visibility into the MCP server’s tool-calling logic.
- **Validation:** All successful verification screenshots in this repository were captured from a local development environment.

## 🧪 Inspector Results Evidence
![analyze_mbagathi_risk output](../../docs/mcp_inspector_test.png)