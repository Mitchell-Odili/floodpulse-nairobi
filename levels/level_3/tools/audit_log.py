import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.cloud import spanner
from uuid import uuid4

# 1. ROBUST PATH DETECTION
# Navigates up from the current file's location to the project root
# parents[2] takes us to the root of 'floodpulse-nairobi'
script_dir = Path(__file__).resolve().parent
root_dir = script_dir.parents[2] # Adjust 'parents' index if folder depth changes
load_dotenv(dotenv_path=root_dir / '.env')

sys.path.append(str(root_dir))

# 2. CLIENT INITIALIZATION
client = spanner.Client(project=os.getenv("PROJECT_ID"))
instance = client.instance(os.getenv("SPANNER_INSTANCE_ID"))
database = instance.database(os.getenv("SPANNER_DATABASE_ID"))

import uuid

def log_event(transaction, responder_id, action_type, resident_id):
    """
    Records the rescue interaction between the responder and the resident.
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