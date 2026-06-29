import os
from pathlib import Path
from google.cloud import spanner
from dotenv import load_dotenv

# Use the robust pathing we established
root_dir = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=root_dir / '.env')

def seed_mbagathi_agents():
    client = spanner.Client(project=os.getenv("PROJECT_ID"))
    instance = client.instance(os.getenv("SPANNER_INSTANCE_ID"))
    database = instance.database(os.getenv("SPANNER_DATABASE_ID"))

    def insert_trinity(transaction):
        # 1. Define Nodes (including placeholder embedding for now)
        # Embedding is ARRAY<FLOAT32>
        node_data = [
            ("node_001", "Sarah", "Resident", 1780.5, "POINT(36.8147 -1.3211)", 0.85, [0.0]*3, "Critical Pulse", "N/A"),
            ("node_002", "Juma", "Responder", 1795.0, "POINT(36.8120 -1.3190)", 0.10, [0.0]*3, "Moderate Pulse", "Available"),
            ("node_003", "Kamau", "Authority", 1810.2, "POINT(36.8100 -1.3150)", 0.05, [0.0]*3, "Low Pulse", "N/A"),
        ]

        edge_data = [
            ("edge_001", "node_001", "node_002", "Path", True, 5.0),
            ("edge_002", "node_002", "node_003", "Main", False, 1.0),
        ]

        transaction.insert_or_update(
            table="Nodes",
            columns=("node_id", "name", "type", "elevation", "location", "current_flash_index", "embedding"),
            values=node_data,
        )

        transaction.insert_or_update(
            table="Edges",
            columns=("edge_id", "start_node_id", "end_node_id", "road_type", "is_flood_prone", "base_weight"),
            values=edge_data,
        )

    database.run_in_transaction(insert_trinity)
    print("🚀 Trinity agents successfully deployed to the Mbagathi Basin.")

if __name__ == "__main__":
    seed_mbagathi_agents()