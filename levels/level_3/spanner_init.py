import os
from google.cloud import spanner
from dotenv import load_dotenv

load_dotenv()

def load_schema_from_file():
    """Reads schema from the local schema.sql now located in Level 3."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(current_dir, "schema.sql")
    
    if not os.path.exists(schema_path):
        print(f"⚠️ schema.sql not found at {schema_path}. Falling back to hardcoded schema.")
        return None

    with open(schema_path, "r", encoding="utf-8") as f:
        full_sql = f.read()

    # Split by semicolon and filter out comments/empty lines
    statements = [
        s.strip() for s in full_sql.split(";") 
        if s.strip() and not s.strip().startswith("--")
    ]
    return statements

# 1. HARDCODED DDL (The Fail-Safe Backup)
MBAGATHI_SCHEMA_BACKUP = [
    """
    CREATE TABLE Nodes (
        node_id STRING(36) NOT NULL,
        name STRING(MAX),
        type STRING(20),
        elevation FLOAT64,
        location STRING(MAX),
        current_flash_index FLOAT64
    ) PRIMARY KEY (node_id)
    """,
    """
    CREATE TABLE Edges (
        edge_id STRING(36) NOT NULL,
        start_node_id STRING(36) NOT NULL,
        end_node_id STRING(36) NOT NULL,
        road_type STRING(20), 
        is_flood_prone BOOL,
        base_weight FLOAT64
    ) PRIMARY KEY (edge_id)
    """,
    """
    CREATE PROPERTY GRAPH FloodResilienceGraph
        NODE TABLES (Nodes)
        EDGE TABLES (
            Edges 
            SOURCE KEY (start_node_id) REFERENCES Nodes (node_id)
            DESTINATION KEY (end_node_id) REFERENCES Nodes (node_id)
            LABEL ConnectedTo
        )
    """
]

def initialize_spanner_graph():
    client = spanner.Client(project=os.getenv("PROJECT_ID"))
    instance = client.instance(os.getenv("SPANNER_INSTANCE_ID"))
    database = instance.database(os.getenv("SPANNER_DATABASE_ID"))

    # 2. Try to load from file first, otherwise use backup
    ddl_statements = load_schema_from_file() or MBAGATHI_SCHEMA_BACKUP

    # Check if DB exists, if not, create it
    if not database.exists():
        print(f"🏗️ Creating database {os.getenv('SPANNER_DATABASE_ID')}...")
        operation = database.create(ddl_statements=ddl_statements)
        operation.result(120)
        print("✅ Database and Graph created.")
        return

    # If DB exists, check for the Nodes table
    try:
        with database.snapshot() as snapshot:
            # A simple ping to see if the schema is actually deployed
            snapshot.execute_sql("SELECT 1 FROM Nodes LIMIT 1").one()
        print("⚠️ Tables already exist. Skipping initialization.")
    except Exception:
        print(f"📊 Table 'Nodes' missing. Initializing with {len(ddl_statements)} statements...")
        operation = database.update_ddl(ddl_statements)
        operation.result(120) 
        print("✅ Level 3: Spanner Graph Repair Online.")

if __name__ == "__main__":
    initialize_spanner_graph()