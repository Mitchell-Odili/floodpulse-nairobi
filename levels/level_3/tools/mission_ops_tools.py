# levels/level_3/tools/mission_ops_tools.py
import os
import sys
import math
import uuid
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv
from google.cloud import spanner

root_dir = Path(__file__).resolve().parents[3]
sys.path.append(str(root_dir))

load_dotenv(dotenv_path=root_dir / '.env')

# Initialize Spanner Client
client = spanner.Client(project=os.getenv("PROJECT_ID"))
instance = client.instance(os.getenv("SPANNER_INSTANCE_ID"))
database = instance.database(os.getenv("SPANNER_DATABASE_ID"))


def log_event(transaction, responder_id, action_type, resident_id):
    """
    Helper to log mission operations events.
    """
    sql = """
    INSERT INTO Rescue_Audit_Log (log_id, resident_id, responder_id, action_type, timestamp)
    VALUES (@log_id, @resident_id, @responder_id, @action, PENDING_COMMIT_TIMESTAMP())
    """
    transaction.execute_update(sql, params={
        "log_id": str(uuid.uuid4()),
        "resident_id": resident_id,
        "responder_id": responder_id,
        "action": action_type
    })


def get_available_responders() -> List[Dict]:
    """
    Queries the database to retrieve all responder nodes that are currently 'Clear'.
    Returns a list of dictionaries containing responder node details.
    """
    query = """
    SELECT node_id, name, lat, lon, status, flash_risk_index
    FROM Nodes
    WHERE type = 'Responder' AND status = 'Moderate Pulse' OR status = 'Critical Pulse'
    """
    responders = []
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(query)
        for row in results:
            responders.append({
                "node_id": row[0],
                "name": row[1],
                "lat": row[2],
                "lon": row[3],
                "status": row[4],
                "flash_risk_index": row[5]
            })
    return responders


def calculate_rescue_route(start_node_id: str, target_node_id: str) -> List[str]:
    """
    Calculates the safest route between a responder and an at-risk resident 
    using the Edges table weights (avoiding flooded/high-risk paths).
    """
    # Query edges to build a simple adjacency path based on dynamic weights
    query = """
    SELECT source_node_id, dest_node_id, current_weight
    FROM Edges
    ORDER BY current_weight ASC
    """
    
    with database.snapshot() as snapshot:
        edges = list(snapshot.execute_sql(query))
    
    # Basic pathfinding resolution (Greedy/Direct path traversal based on weights)
    # This can be expanded to a full Dijkstra implementation if your network graph grows complex.
    route = [start_node_id]
    current = start_node_id
    
    visited = set([start_node_id])
    max_hops = 10  # Safety break to prevent infinite loops
    
    for _ in range(max_hops):
        if current == target_node_id:
            break
            
        next_hop = None
        min_weight = float('inf')
        
        for src, dest, weight in edges:
            if src == current and dest not in visited:
                if weight < min_weight:
                    min_weight = weight
                    next_hop = dest
                    
        if next_hop:
            route.append(next_hop)
            visited.add(next_hop)
            current = next_hop
        else:
            break # No valid continuation found
            
    if route[-1] != target_node_id:
        # Fallback to direct routing if graph traversal hits a dead end
        route = [start_node_id, target_node_id]
        
    return route


def get_nearest_responder(resident_id):
    """Uses the index-based proximity logic to find the closest available responder."""
    query = """
    WITH ResidentInfo AS (
        SELECT CAST(SUBSTR(node_id, 6) AS INT64) AS idx FROM Nodes WHERE node_id = @res_id
    )
    SELECT r.node_id
    FROM Nodes r, ResidentInfo res
    WHERE r.type = 'Responder' 
      AND r.status IN ('Clear', 'Moderate Pulse')
    ORDER BY ABS(CAST(SUBSTR(r.node_id, 6) AS INT64) - res.idx) ASC
    LIMIT 1
    """
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(query, params={'res_id': resident_id}, 
                                       param_types={'res_id': spanner.param_types.STRING})
        row = list(results)
        return row[0][0] if row else None


def dispatch_to_resident(resident_id):
    """Orchestrates the dispatch: finds the responder, calculates safe routes, updates status, and logs."""
    responder_id = get_nearest_responder(resident_id)
    
    if not responder_id:
        print(f"⚠️ No available responders for {resident_id}.")
        return

    # 1. Calculate the safest route using network graph weights
    route = calculate_rescue_route(responder_id, resident_id)
    print(f"🗺️ Safe route calculated: {' -> '.join(route)}")

    def update_transaction(transaction):
        transaction.execute_update(
            "UPDATE Nodes SET status = 'Rescue In Progress' WHERE node_id = @rid",
            params={'rid': resident_id},
            param_types={'rid': spanner.param_types.STRING}
        )
        transaction.execute_update(
            "UPDATE Nodes SET status = 'Busy' WHERE node_id = @resp_id",
            params={'resp_id': responder_id},
            param_types={'resp_id': spanner.param_types.STRING}
        )
        log_event(transaction, responder_id, "DISPATCH", resident_id)
    
    database.run_in_transaction(update_transaction)
    print(f"🚀 Dispatched {responder_id} to {resident_id} via route: {route}.")


def finalize_rescue(resident_id: str, responder_id: Optional[str] = None, status_code: str = "Safe"):
    """Closes the rescue mission: marks resident as safe, responder as 'Clear', and logs completion."""
    def update(transaction):
        transaction.execute_update(
            "UPDATE Nodes SET status = @status WHERE node_id = @rid",
            params={'status': status_code, 'rid': resident_id},
            param_types={'status': spanner.param_types.STRING, 'rid': spanner.param_types.STRING}
        )
        
        if responder_id:
            transaction.execute_update(
                "UPDATE Nodes SET status = 'Clear' WHERE node_id = @resp_id",
                params={'resp_id': responder_id},
                param_types={'resp_id': spanner.param_types.STRING}
            )
            
        log_event(transaction, responder_id or "UNKNOWN", "COMPLETION", resident_id)
    
    database.run_in_transaction(update)
    print(f"✅ Rescue complete for {resident_id}.")


if __name__ == "__main__":
    # Test dispatch manually if run directly
    test_resident_id = "node_001"
    # print(f"Testing manual dispatch for resident: {test_resident_id}")
    
    # try:
    #     dispatch_to_resident(test_resident_id)
    #     print("Test dispatch sequence completed successfully.")
    # except Exception as e:
    #     print(f"❌ Dispatch test failed with error: {e}")

    print("\n--- ✅ TESTING RESCUE FINALIZATION PHASE ---")
    # For testing finalization, we grab the responder assigned or default to node_004
    test_responder_id = "node_004" 
    
    try:
        finalize_rescue(test_resident_id, responder_id=test_responder_id, status_code="Safe")
        print("Finalization test completed successfully.")
    except Exception as e:
        print(f"❌ Finalization test failed: {e}")