import os
import math
import uuid
import random
from pathlib import Path
from google.cloud import spanner
from dotenv import load_dotenv

# Path configuration
root_dir = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=root_dir / '.env')

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def seed_mbagathi_agents():
    client = spanner.Client(project=os.getenv("PROJECT_ID"))
    instance = client.instance(os.getenv("SPANNER_INSTANCE_ID"))
    database = instance.database(os.getenv("SPANNER_DATABASE_ID"))

    name_pool = [
        "Amina", "Kofi", "Fatuma", "Otieno", "Wanjiku", "Mwangi", "Abdi", 
        "Chebet", "Omondi", "Njeri", "Juma", "Kamau", "Sarah", "Benson", 
        "Linet", "Elias", "Faith", "Samuel", "Grace", "David", "Esther", "Peter"
    ]
    random_names = random.sample(name_pool, 22)

    # 1. Define specific core actors
    nodes = [
        {'node_id': 'node_001', 'name': 'Sarah', 'type': 'Resident', 'lat': -1.3100, 'lon': 36.8100, 'elev': 1700.0},
        {'node_id': 'node_002', 'name': 'Juma', 'type': 'Responder', 'lat': -1.3110, 'lon': 36.8110, 'elev': 1705.0},
        {'node_id': 'node_003', 'name': 'Kamau', 'type': 'Authority', 'lat': -1.3120, 'lon': 36.8120, 'elev': 1710.0},
    ]
    
    # 2. Add 4 additional Responders (i=4 to 7) and Residents (i=8 to 25)
    for i in range(4, 26):
        node_type = 'Responder' if i < 8 else 'Resident'
        nodes.append({
            'node_id': f'node_{i:03}', 
            'name': random_names[i-4], 
            'type': node_type, 
            'lat': round(-1.3120 + (i*0.002), 4), 
            'lon': round(36.8120 + (i*0.002), 4),
            'elev': round(1710.0 + (i * 2.5), 2) # Simulated terrain slope
        })

    # 3. Batch Insert Nodes (Updated for 'elevation' column)
    with database.batch() as batch:
        batch.insert("Nodes", 
            ["node_id", "name", "type", "lat", "lon", "elevation", "status", "flash_risk_index"],
            [(n['node_id'], n['name'], n['type'], n['lat'], n['lon'], n['elev'], 'Clear', 0.0) for n in nodes]
        )

    # 4. Create and Insert Edges
    edges = []
    for i in range(len(nodes) - 1):
        dist = calculate_haversine_distance(nodes[i]['lat'], nodes[i]['lon'], nodes[i+1]['lat'], nodes[i+1]['lon'])
        edges.append({'edge_id': f'edge_{i:03}', 'start': nodes[i]['node_id'], 'end': nodes[i+1]['node_id'], 'dist': dist})

    with database.batch() as batch:
        batch.insert("Edges", 
            ["edge_id", "source_node_id", "dest_node_id", "base_weight", "current_weight", "is_flood_prone"],
            [(e['edge_id'], e['start'], e['end'], e['dist'], e['dist'], False) for e in edges]
        )

    print(f"✅ Seeded {len(nodes)} nodes with elevation data and {len(edges)} edges.")

if __name__ == "__main__":
    seed_mbagathi_agents()