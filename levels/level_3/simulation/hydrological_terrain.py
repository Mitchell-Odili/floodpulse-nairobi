import os
import sys
import math
from pathlib import Path
from dotenv import load_dotenv
from google.cloud import spanner

root_dir = Path(__file__).resolve().parents[3]
sys.path.append(str(root_dir))

from levels.level_3.tools.agent_logic import get_risk_adjustment
from levels.level_3.tools.geo_engine import GeoEngine

load_dotenv(dotenv_path=root_dir / '.env')


# 1. UPDATED INFRASTRUCTURE UPDATE
def update_edge_weights(transaction, intensity):
    """Updates edge costs based on storm intensity."""
    query = """
        UPDATE Edges 
        SET current_weight = base_weight * (1 + (CAST(is_flood_prone AS INT64) * @intensity * 5.0))
        WHERE TRUE
    """
    transaction.execute_update(
        query, 
        params={'intensity': intensity},
        param_types={'intensity': spanner.param_types.FLOAT64} 
    )

# 2. BATCH UPDATE TRANSACTION
def _bulk_update(transaction, updates, storm_intensity):
    for u in updates:
        # Status Guard: Skips nodes currently in a rescue mission
        transaction.execute_update(
            """
            UPDATE Nodes 
            SET flash_risk_index = @v, status = @s 
            WHERE node_id = @id AND status != 'Rescue In Progress'
            """,
            params={"v": u["v"], "s": u["s"], "id": u["id"]}
        )
    
    update_edge_weights(transaction, storm_intensity)

def run_basin_impact_simulation(project_id, instance_id, database_id, storm_center_lat, storm_center_lon):
    """
    Simulates hydrological risk propagation based on terrain and storm proximity.
    Updates the basin's node-edge state in Spanner.
    """
    
    client = spanner.Client(project=project_id)
    instance = client.instance(instance_id)
    database = instance.database(database_id)

    engine = GeoEngine()
    storm_center = {'lat': storm_center_lat, 'lon': storm_center_lon}
    storm_intensity = 0.25
    
    # 3. FETCH STATE
    query = "SELECT node_id, type, flash_risk_index, status, lat, lon FROM Nodes"
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(query)
        nodes = list(results)
    
    updates = []
    
    # 4. COMPUTE RISK
    for node in nodes:
        node_id, n_type, curr_idx, status, lat, lon = node
        
        # Only simulate nodes that aren't already being rescued
        if status == 'Rescue In Progress':
            continue
            
        elev = engine.get_elevation(lat, lon)
        
        # Calculate spatial decay
        dist = math.sqrt((storm_center['lat'] - lat)**2 + (storm_center['lon'] - lon)**2)
        intensity = storm_intensity * math.exp(-dist * 10)
            
        # Agent Logic
        new_idx, new_status = get_risk_adjustment(n_type, curr_idx, intensity, elev)
        
        updates.append({"id": node_id, "v": new_idx, "s": new_status})

    # 5. EXECUTE BATCH
    if updates:
        database.run_in_transaction(_bulk_update, updates, storm_intensity)
        print(f"✅ Simulation complete: {len(updates)} agents updated.")

if __name__ == "__main__":
    run_basin_impact_simulation(
        os.getenv("PROJECT_ID"), 
        os.getenv("SPANNER_INSTANCE_ID"), 
        os.getenv("SPANNER_DATABASE_ID"),
        -1.3200, 36.8150
    )