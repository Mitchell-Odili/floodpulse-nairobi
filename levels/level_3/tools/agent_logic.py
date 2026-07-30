from google.cloud import spanner
from google.cloud.spanner_v1 import param_types

def get_risk_adjustment(node_type, current_index, intensity, elevation):
    """Calculates risk based on agent role, weather intensity, and elevation."""
    if node_type == 'Authority':
        return 0.05, "Clear" 
    
    # 2. Determine sensitivity multiplier based on type
    # Residents might be more vulnerable than Responders
    sensitivity = 1.5 if node_type == 'Resident' else 1.0

    # Elevation factor: Lower elevation increases risk
    elevation_factor = max(1.0, (1800 - elevation) / 100)
    adjusted_intensity = (intensity * elevation_factor) * sensitivity
    
    new_index = max(0.0, min(1.0, current_index + adjusted_intensity - (0.02 if intensity < 0.08 else 0.0)))
    
    # Map to schema status
    if new_index <= 0.2: status = "Clear"
    elif new_index <= 0.6: status = "Moderate Pulse"
    else: status = "Critical Pulse"
        
    return new_index, status

def get_critical_nodes(database):
    """
    Retrieves all nodes that are currently in a 'Critical Pulse' state.
    Returns a list of node objects/dictionaries for the orchestrator to process.
    """
    query = """
        SELECT node_id, name, status, flash_risk_index 
        FROM Nodes 
        WHERE status = 'Critical Pulse'
    """
    
    nodes = []
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(query)
        for row in results:
            nodes.append({
                "node_id": row[0],
                "name": row[1],
                "status": row[2],
                "flash_risk_index": row[3]
            })
    return nodes
    

def update_agent_risk(database, node_id, node_type, current_index, intensity, elevation):
    final_index, final_status = get_risk_adjustment(node_type, current_index, intensity, elevation)

    def _do_update(transaction):
        update_statement = """
            UPDATE Nodes 
            SET flash_risk_index = @new_val,
                status = @new_status
            WHERE node_id = @id
        """
        transaction.execute_update(
            update_statement,
            params={
                "new_val": final_index, 
                "new_status": final_status, 
                "id": node_id
            },
            param_types={
                "new_val": param_types.FLOAT64,
                "new_status": param_types.STRING,
                "id": param_types.STRING
            },
        )
        
        if final_status == "Critical Pulse":
            print(f"🚨 CRITICAL ALERT: {node_id} reached Critical status.")

    database.run_in_transaction(_do_update)

def get_agent_status(database, node_id):
    query = "SELECT name, type, flash_risk_index, status FROM Nodes WHERE node_id = @id"
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            query, 
            params={"id": node_id}, 
            param_types={"id": param_types.STRING}
        )
        return list(results)