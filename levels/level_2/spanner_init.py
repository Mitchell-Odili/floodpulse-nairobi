import os
from pathlib import Path
from google.cloud import spanner
from dotenv import load_dotenv

# Path configuration
script_dir = Path(__file__).resolve().parent
root_dir = script_dir.parent.parent
dotenv_path = root_dir / '.env'

# Load credentials from .env
load_dotenv(dotenv_path=dotenv_path)

def load_schema_from_file(directory):
    schema_path = directory / "schema.sql"
    
    with open(schema_path, "r", encoding="utf-8") as f:
        full_sql = f.read()
    
    # 1. Print the content to confirm what it actually sees
    print(f"DEBUG: Content head: {full_sql[:100]}...") 

    # 2. Use a more robust split, and don't filter out things so aggressively
    # We remove lines that are just comments, but keep the core SQL
    statements = [
        s.strip() for s in full_sql.split(";") 
        if len(s.strip()) > 10 # Only keep statements longer than 10 characters
    ]
    
    print(f"DEBUG: Found {len(statements)} statements after cleaning.")
    return statements

def initialize_spanner_graph(script_dir):

    # Retrieve and validate variables
    project_id = os.getenv("PROJECT_ID")
    instance_id = os.getenv("SPANNER_INSTANCE_ID")
    db_id = os.getenv("SPANNER_DATABASE_ID")

    if not all([project_id, instance_id, db_id]):
        raise ValueError(f"Missing environment variables! Got: P={project_id}, I={instance_id}, DB={db_id}")

    client = spanner.Client(project=os.getenv("PROJECT_ID"))
    instance = client.instance(os.getenv("SPANNER_INSTANCE_ID"))
    
    # Fetch the schema first
    ddl_statements = load_schema_from_file(script_dir)
    if not ddl_statements:
        print("❌ Initialization aborted: No schema defined.")
        return

    # Define the database object WITH the ddl_statements
    database = instance.database(os.getenv("SPANNER_DATABASE_ID"), ddl_statements=ddl_statements)

    if not database.exists():
        print(f"🏗️ Creating database {os.getenv('SPANNER_DATABASE_ID')}...")
        # 3. Now call create() with NO arguments
        operation = database.create()
        operation.result(120)
        print("✅ Database, Tables, and Graph created from schema.sql.")
    else:
        # 2. Check for missing embedding column (Evolution)
        print("🔍 Checking schema status...")
        with database.snapshot() as snapshot:
            query = "SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Nodes' AND COLUMN_NAME = 'embedding'"
            if not list(snapshot.execute_sql(query)):
                print("🔄 Updating Schema: Adding missing embedding column...")
                op = database.update_ddl(["ALTER TABLE Nodes ADD COLUMN embedding ARRAY<FLOAT32>"])
                op.result(60)
                print("✅ Schema evolved successfully.")
            else:
                print("✨ Schema is up to date.")

if __name__ == "__main__":
    initialize_spanner_graph(script_dir)