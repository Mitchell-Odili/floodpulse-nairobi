-- 1. Nodes: Now including the 'Live Pulse' column
CREATE TABLE Nodes (
    node_id STRING(36) NOT NULL,
    name STRING(MAX),
    type STRING(20), -- 'Ridge', 'Sump', 'Intersection'
    elevation FLOAT64,
    location STRING(MAX),
    current_flash_index FLOAT64 -- <--- Fused from Level 2 Telemetry
) PRIMARY KEY (node_id);

-- 2. Edges: The Connections
CREATE TABLE Edges (
    edge_id STRING(36) NOT NULL,
    start_node_id STRING(36) NOT NULL,
    end_node_id STRING(36) NOT NULL,
    road_type STRING(20), 
    is_flood_prone BOOL,
    base_weight FLOAT64 -- <--- Strategic cost of travel
) PRIMARY KEY (edge_id);

-- 3. Property Graph Definition (The AI's Navigation Map)
CREATE PROPERTY GRAPH FloodResilienceGraph
    NODE TABLES (Nodes)
    EDGE TABLES (
        Edges 
        SOURCE KEY (start_node_id) REFERENCES Nodes (node_id)
        DESTINATION KEY (end_node_id) REFERENCES Nodes (node_id)
        LABEL ConnectedTo
    );