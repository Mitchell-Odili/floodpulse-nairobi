# Level 3: The Digital Guardian (Spanner Graph Infrastructure)

## 📌 Overview
Level 3 transitions the **FloodPulse** project from local data structures to a production-grade, cloud-native **Google Cloud Spanner Property Graph**. This layer serves as the "Digital Guardian," providing the relational intelligence required to navigate emergency response paths in the Mbagathi Basin.

## 🏗️ Architectural Components

### 1. Spanner Property Graph
We implemented a heterogeneous graph using the **Spanner Graph** engine. This allows for complex traversals (finding paths from residents to authorities) without the performance overhead of traditional SQL joins.
* **Nodes**: Represent Residents (Sarah), Responders (Juma), and Authorities (Kamau).
* **Edges**: Represent physical or social connections (`ConnectedTo`) with metadata like `road_type` and `is_flood_prone`.

### 2. Idempotent Initialization (`spanner_init.py`)
The infrastructure layer features a "Smart Repair" logic:
* **Database Check**: Verifies the existence of the Spanner database container.
* **Schema Audit**: Performs a "ping" on the `Nodes` table. If missing, it automatically restores the schema using a local `schema.sql` file with a hardcoded DDL backup for maximum resilience.

### 3. Trinity Agent Seeding (`seed_data.py`)
This script populates the network with our core personas using ACID-compliant transactions. 
* **Sarah (Resident)**: Located in a high-risk sump area (`flash_index: 0.85`).
* **Juma (Responder)**: Strategically positioned near Sarah.
* **Kamau (Authority)**: The central hub for coordination.

---

## 🚀 Quick Start

### Prerequisites
* Google Cloud Spanner instance named `survivor-network`.
* Environment variables configured in `.env` (`PROJECT_ID`, `SPANNER_INSTANCE_ID`, etc.).

### Deployment
1. **Initialize Infrastructure**:
   ```powershell
   python levels/level_3/spanner_init.py

*If tables exist, the script will safely skip initialization.*

2. **Seed Data**
   ```powershell
   python levels/level_3/seed_data.py

### 🔍 Verification Queries
To verify the graph traversal, run the following GQL in Spanner Studio:
``` SQL
SELECT * FROM GRAPH_TABLE(FloodResilienceGraph 
   MATCH (r:Nodes)-[e:ConnectedTo]->(res:Nodes)
   WHERE r.current_flash_index > 0.7
   RETURN 
      r.name AS AtRiskResident, 
      r.current_flash_index AS RiskLevel,
      res.name AS AssignedResponder
); 

### 🛠️ Technical Decisions & Pivots
- **Spatial Data Type:** Pivoted from `ST_GEOMETRY` to `STRING(MAX)` for the `location` column to ensure environment compatibility while maintaining Well-Known Text (WKT) standards.
- Colocation: Moved `schema.sql` into the level_3 directory to create a self-contained, modular deployment package.

Status: Level 3 Fully Operational | Region: Nairobi, Kenya (NBO)
