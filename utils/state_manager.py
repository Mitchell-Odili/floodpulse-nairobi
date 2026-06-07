import json
import os

REGISTRY_PATH = os.path.join("data", "registry.json")

def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        return {}
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)

def save_registry(registry):
    os.makedirs("data", exist_ok=True)
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=4)

def update_registry(responder_name, data):
    registry = load_registry()
    registry[responder_name] = data
    save_registry(registry)