-- 1. Create the Nodes (Points of Interest)
-- This stores the 'Safe Ridges' and 'Low-lying Sumps'
CREATE TABLE Nodes (
    node_id STRING(36) NOT NULL,
    name STRING(MAX),
    type STRING(20), -- 'Ridge', 'Sump', 'Intersection'
    elevation FLOAT64,
    location GEOGRAPHY
) PRIMARY KEY (node_id);

-- 2. Create the Edges (The Connections)
-- This stores the roads connecting the nodes
CREATE TABLE Edges (
    edge_id STRING(36) NOT NULL,
    start_node_id STRING(36) NOT NULL,
    end_node_id STRING(36) NOT NULL,
    road_type STRING(20), -- 'Paved', 'Dirt', 'Path'
    is_flood_prone BOOL
) PRIMARY KEY (edge_id);

-- 3. The Property Graph Definition
-- This tells Spanner to treat these tables as a searchable network
CREATE PROPERTY GRAPH FloodResilienceGraph
    NODE TABLES (Nodes)
    EDGE TABLES (Edges 
        SOURCE KEY (start_node_id) REFERENCES Nodes (node_id)
        DESTINATION KEY (end_node_id) REFERENCES Nodes (node_id)
    );