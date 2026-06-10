#!/bin/bash
# FloodPulse Studio Setup Script
# Initializes the environment for Level 1 Synthesis

echo "================================================================"
echo "FloodPulse: Studio Engine Environment Setup"
echo "================================================================"

# [1/3] Verification
echo "[1/3] Verifying Project Structure..."

# Move up to the project root from level_1/setup/
cd ../.. 

if [ ! -d "sandbox" ]; then
    echo "Error: 'sandbox/' directory not found at project root."
    exit 1
fi
echo "      ✓ Sandbox/ Diagnostic folder verified"

# [2/3] Dependency Check
echo "[2/3] Checking Dependencies..."
if ! command -v uv &> /dev/null; then
    echo "Error: 'uv' not found. Please install via https://github.com/astral-sh/uv"
    exit 1
fi
echo "      ✓ uv (Package Manager) found"

# [3/3] Configuration
echo "[3/3] Initializing Mission Registry..."
# Create data dir if not exists
mkdir -p data
if [ ! -f "data/registry.json" ]; then
    echo "{}" > data/registry.json
fi
echo "      ✓ Registry initialized at data/registry.json"

echo "================================================================"
echo "✅ Studio Engine Ready for Synthesis!"
echo "================================================================"