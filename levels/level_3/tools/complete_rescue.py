import os
import sys
from google.cloud import spanner
from pathlib import Path
from dotenv import load_dotenv

# 1. ROBUST PATH RESOLUTION
script_dir = Path(__file__).resolve().parent
root_dir = script_dir.parents[2] 
load_dotenv(dotenv_path=root_dir / '.env')

sys.path.append(str(root_dir))

from levels.level_3.tools.audit_log import log_event


# 2. CLIENT INITIALIZATION
client = spanner.Client(project=os.getenv("PROJECT_ID"))
instance = client.instance(os.getenv("SPANNER_INSTANCE_ID"))
database = instance.database(os.getenv("SPANNER_DATABASE_ID"))

# 1. REMOVE the global database variable at the top
# We will use the database passed into the function instead.

def finalize_rescue(database, resident_id, responder_id=None, status_code="Safe"):
    """
    Closes the rescue mission: marks resident as safe, responder as 'Clear', 
    and logs the completion.
    """
    def update(transaction):
        # Update Resident
        transaction.execute_update(
            "UPDATE Nodes SET status = @status WHERE node_id = @rid",
            params={'status': status_code, 'rid': resident_id}
        )
        
        # Update Responder
        if responder_id:
            transaction.execute_update(
                "UPDATE Nodes SET status = 'Clear' WHERE node_id = @resp_id",
                params={'resp_id': responder_id}
            )
            
        # Log event
        log_event(transaction, responder_id, "COMPLETION", resident_id)
    
    # 2. Use the 'database' passed as an argument
    database.run_in_transaction(update)
    print(f"✅ Rescue complete for {resident_id}.")

    
if __name__ == "__main__":
    # Example usage
    target_resident = "node_008"
    target_responder = "node_007"
    finalize_rescue(target_resident, target_responder)