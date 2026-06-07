# FloodPulse Sandbox
This directory serves as the **experimental workspace** for the FloodPulse project. It contains live MCP (Model Context Protocol) test rigs and diagnostic tools used to validate agentic reasoning and tool integration.

## 🧪 Purpose
- **Tool Validation:** Testing the integration between the MCP Inspector, Gemini models, and the project's internal tools (e.g., `tools/weather_tools.py`).
- **Experimental Rigging:** Iterating on connection logic (ADC vs. API-based authentication) without impacting the production engine in `levels/.`
- **Lab Logging:** Documenting lessons learned, architecture discoveries, and troubleshooting notes.

## 📂 Contents
- `adc_vision_mcp.py:` Production-aligned MCP server using Google Cloud Application Default Credentials (ADC).
- `vision_mcp.py:` Experimental MCP server using standard API keys, ideal for rapid prototyping and bypassing project-specific model quotas.
- `notes.md:` A comprehensive lab log detailing experiment results, authentication struggles, port configurations (6274), and model availability findings.

## 🚀 Getting Started
To interact with these tools, use the MCP Inspector:

1. Install the Inspector:
```
Bash
npm install -g @modelcontextprotocol/inspector
```
2. Launch a test rig:
```
Bash
# Replace the file name with the rig you want to test
npx @modelcontextprotocol/inspector uv run sandbox/adc_vision_mcp.py
```
3. Verify: Open the local dashboard at `http://localhost:6274` to execute tools and review responses.

## 🛠️ Operational Notes
- **Path Resolution:** These scripts use dynamic pathing to locate the `PROJECT_ROOT.` Ensure your `config.json` is present in the root of the project for ADC scripts to function correctly.
- **Environment:** All successful tests recorded in `notes.md` were performed in a local VS Code environment. Remote cloud development environments (like Cloud Shell) may face tunneling restrictions with the Inspector.