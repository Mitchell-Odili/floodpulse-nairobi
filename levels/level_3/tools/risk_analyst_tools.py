# level_3/tools/risk_analyst_tools.py
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.cloud import spanner
from typing import List, Optional, Dict

root_dir = Path(__file__).resolve().parents[3]
sys.path.append(str(root_dir))

from levels.level_3.models.assessment import NodeTelemetry

load_dotenv(dotenv_path=root_dir / '.env')

def query_basin_risk_state() -> List[NodeTelemetry]:
    """Queries Spanner to get the full telemetry for all nodes in the basin."""
    client = spanner.Client(project=os.getenv("PROJECT_ID"))
    db = client.instance(os.getenv("SPANNER_INSTANCE_ID")).database(os.getenv("SPANNER_DATABASE_ID"))
    
    query = """
        SELECT node_id, name, type, lat, lon, elevation, status, flash_risk_index 
        FROM Nodes
    """
    
    nodes = []
    with db.snapshot() as snapshot:
        results = snapshot.execute_sql(query)
        for row in results:
            nodes.append(NodeTelemetry(
                node_id=row[0],
                name=row[1],
                node_type=row[2],
                lat = row[3],
                lon = row[4],
                elevation_m=row[5],
                risk_level=row[6],
                flash_risk_index=row[7],

            ))
            
    return nodes


def query_node_by_name(name: str) -> List[NodeTelemetry]:
    """Queries Spanner and returns all matching nodes for a given name."""
    client = spanner.Client(project=os.getenv("PROJECT_ID"))
    db = client.instance(os.getenv("SPANNER_INSTANCE_ID")).database(os.getenv("SPANNER_DATABASE_ID"))
    
    query = """
        SELECT node_id, name, type, lat, lon, elevation, status, flash_risk_index 
        FROM Nodes 
        WHERE name = @name
    """
    params = {"name": name}
    param_types = {"name": spanner.param_types.STRING}

    nodes = []
    with db.snapshot() as snapshot:
        results = snapshot.execute_sql(query, params=params, param_types=param_types)
        for row in results:
            nodes.append(NodeTelemetry(
                node_id=row[0],
                name=row[1],
                node_type=row[2],
                lat = row[3],
                lon = row[4],
                elevation_m=row[5],
                risk_level=row[6],
                flash_risk_index=row[7],
            ))
            
    return nodes


if __name__ == "__main__":
    print("--- Testing Basin Risk State ---")
    basin_state = query_basin_risk_state()
    print(f"Total nodes fetched: {len(basin_state)}")
    print(basin_state[:3]) # Print first 3 nodes as a sample
    
    print("\n--- Testing Query Node by Name ---")
    test_name = "Sarah" 
    node_result = query_node_by_name(test_name)
    print(f"Result for '{test_name}': {node_result}")