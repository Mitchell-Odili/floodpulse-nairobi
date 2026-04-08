import os
from google.cloud import spanner
from dotenv import load_dotenv

load_dotenv()

def seed_mbagathi_agents():
    client = spanner.Client(project=os.getenv("PROJECT_ID"))
    instance = client.instance(os.getenv("SPANNER_INSTANCE_ID"))
    database = instance.database(os.getenv("SPANNER_DATABASE_ID"))

    def insert_trinity(transaction):
        # 1. Define the Residents (Nodes)
        # Columns: node_id, name, type, elevation, location, current_flash_index
        node_data = [
            ("node_001", "Sarah", "Resident", 1780.5, "POINT(36.8147 -1.3211)", 0.85),
            ("node_002", "Juma", "Responder", 1795.0, "POINT(36.8120 -1.3190)", 0.10),
            ("node_003", "Kamau", "Authority", 1810.2, "POINT(36.8100 -1.3150)", 0.05),
        ]

        # 2. Define the Relationships (Edges)
        # Columns: edge_id, start_node_id, end_node_id, road_type, is_flood_prone, base_weight
        edge_data = [
            ("edge_001", "node_001", "node_002", "Path", True, 5.0), # Sarah connected to Juma
            ("edge_002", "node_002", "node_003", "Main", False, 1.0), # Juma connected to Kamau
        ]

        # Execute Inserts - Note the added "location" in columns
        transaction.insert_or_update(
            table="Nodes",
            columns=("node_id", "name", "type", "elevation", "location", "current_flash_index"),
            values=node_data,
        )

        transaction.insert_or_update(
            table="Edges",
            columns=("edge_id", "start_node_id", "end_node_id", "road_type", "is_flood_prone", "base_weight"),
            values=edge_data,
        )

    # Run the transaction
    database.run_in_transaction(insert_trinity)
    print("🚀 Trinity agents successfully deployed to the Mbagathi Basin.")

if __name__ == "__main__":
    seed_mbagathi_agents()