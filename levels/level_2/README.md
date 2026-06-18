# Level 2: The Digital Guardian (Spanner Graph Infrastructure)

## 📌 Overview
Level 2 transitions the **FloodPulse** project from local data structures to a production-grade, cloud-native **Google Cloud Spanner Property Graph**. This layer serves as the "Digital Guardian," providing the relational intelligence required to navigate emergency response paths in the Mbagathi Basin.

## 🏗️ Architectural Components

### 1. Spanner Property Graph
We implemented a heterogeneous graph using the **Spanner Graph** engine. This allows for complex traversals (finding paths from residents to authorities) without the performance overhead of traditional SQL joins.
* **Nodes**: Represent Residents (Sarah), Responders (Juma), and Authorities (Kamau).
* **Edges**: Represent physical or social connections (`ConnectedTo`) with metadata like `road_type` and `is_flood_prone`.

### 2. Embedding Strategy
The `Nodes` table includes an `embedding` column defined as ARRAY<FLOAT32>.
- **Purpose:** This column is reserved for vector representations of spatial and persona-based data.
- **Current State:** Initialized with placeholder zeros; this serves as the foundational hook for upcoming integration with vector search engines and LLM-driven agent decision-making.

### 3. Idempotent Initialization (`spanner_init.py`)
The infrastructure layer features a "Smart Repair" logic:
* **Database Check**: Verifies the existence of the Spanner database container.
* **Schema Audit**: Performs a health check on the schema. If tables are missing, it dynamically reads and applies the structure from the [`schema.sql`](schema.sql) file.

### 4. Trinity Agent Seeding (`seed_data.py`)
This script populates the network with our core personas using ACID-compliant transactions. 
* **Sarah (Resident)**: Located in a high-risk sump area (`flash_index: 0.85`).
* **Juma (Responder)**: Strategically positioned near Sarah.
* **Kamau (Authority)**: The central hub for coordination.

---

## 🚀 Quick Start

### Prerequisites
* Google Cloud Spanner instance e.g. `floodpulse-nairobi-lab`.
### Environment
* Ensure your root `.env` file contains the following configuration:
```PROJECT_ID=floodpulse-nairobi
SPANNER_INSTANCE_ID=floodpulse-nairobi-lab
SPANNER_DATABASE_ID=floodpulse-db
```

### Deployment
1. **Initialize Infrastructure**:
   ```powershell
   uv run levels/level_2/spanner_init.py

*If tables exist, the script will safely skip initialization.*

2. **Seed Data**
   ```powershell
   uv run levels/level_2/seed_data.py

### 🔍 Verification Queries
To verify the graph traversal, run the following GQL in Spanner Studio:

```sql
SELECT * FROM GRAPH_TABLE(FloodResilienceGraph 
   MATCH (r:Nodes)-[e:ConnectedTo]->(res:Nodes)
   WHERE r.current_flash_index > 0.7
   RETURN 
      r.name AS AtRiskResident, 
      r.current_flash_index AS RiskLevel,
      res.name AS AssignedResponder
);
```

### 🛠️ Technical Decisions & Pivots
- **Spatial Data Type:** Pivoted to `STRING(MAX)` for WKT (Well-Known Text) compatibility, ensuring the infrastructure remains lightweight and portable.
- **Modularity:** Moved all schema definitions into a self-contained [`schema.sql`](schema.sql) within the component directory, ensuring the code remains strictly decoupled from the underlying database definition. This design allows for modular updates to the schema without requiring modifications to the core initialization logic.
- **Evolutionary Schema:** The `spanner_init.py` script includes an "Evolutionary" check, specifically scanning for the `embedding` column and applying `ALTER TABLE` statements automatically if the schema is updated in the future.
---
Status: Level 2 Fully Operational | Region: Nairobi, Kenya (NBO)
