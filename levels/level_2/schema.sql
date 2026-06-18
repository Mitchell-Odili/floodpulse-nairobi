-- 1. NODES TABLE
-- Stores individual points of interest in the Mbagathi Basin
CREATE TABLE Nodes (
    node_id STRING(36) NOT NULL,
    name STRING(MAX),
    type STRING(20), -- e.g., 'Ridge', 'Sump', 'Intersection', 'Residential'
    elevation FLOAT64,
    location STRING(MAX), -- JSON or Coordinate string
    current_flash_index FLOAT64,
    -- Future-proofing: Vector storage for AI semantic search
    embedding ARRAY<FLOAT32> 
) PRIMARY KEY (node_id);

-- 2. EDGES TABLE
-- Stores the connectivity between nodes, defining the navigation paths
CREATE TABLE Edges (
    edge_id STRING(36) NOT NULL,
    start_node_id STRING(36) NOT NULL,
    end_node_id STRING(36) NOT NULL,
    road_type STRING(20), 
    is_flood_prone BOOL,
    base_weight FLOAT64 -- Strategic cost factor for agents to calculate routes
) PRIMARY KEY (edge_id);

-- 3. PROPERTY GRAPH DEFINITION
-- This creates the 'AI's View' of the relational data above
CREATE PROPERTY GRAPH FloodResilienceGraph
    NODE TABLES (Nodes)
    EDGE TABLES (
        Edges 
        SOURCE KEY (start_node_id) REFERENCES Nodes (node_id)
        DESTINATION KEY (end_node_id) REFERENCES Nodes (node_id)
        LABEL ConnectedTo
    );