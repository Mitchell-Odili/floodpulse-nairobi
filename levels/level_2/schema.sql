CREATE TABLE Nodes (
    node_id STRING(MAX) NOT NULL,
    name STRING(MAX) NOT NULL,
    type STRING(MAX) NOT NULL,
    lat FLOAT64 NOT NULL,
    lon FLOAT64 NOT NULL,
    elevation FLOAT64 NOT NULL,
    status STRING(MAX) DEFAULT ('Clear'),
    flash_risk_index FLOAT64 DEFAULT (0.0),
    last_updated TIMESTAMP OPTIONS (allow_commit_timestamp = true)
) PRIMARY KEY (node_id);


CREATE TABLE Edges (
    edge_id STRING(MAX) NOT NULL,
    source_node_id STRING(MAX) NOT NULL,
    dest_node_id STRING(MAX) NOT NULL,
    base_weight FLOAT64 NOT NULL,
    current_weight FLOAT64 NOT NULL,
    is_flood_prone BOOL DEFAULT (FALSE),
    CONSTRAINT FK_Source FOREIGN KEY (source_node_id) REFERENCES Nodes(node_id),
    CONSTRAINT FK_Dest FOREIGN KEY (dest_node_id) REFERENCES Nodes(node_id)
) PRIMARY KEY (edge_id);


CREATE TABLE Node_Embeddings (
    node_id STRING(MAX) NOT NULL,
    embedding ARRAY<FLOAT64>,
    context_description STRING(MAX),
    CONSTRAINT FK_Node_Embed FOREIGN KEY (node_id) REFERENCES Nodes(node_id)
) PRIMARY KEY (node_id);


CREATE TABLE Rescue_Audit_Log (
    log_id STRING(36) NOT NULL,
    resident_id STRING(MAX) NOT NULL, -- The subject
    responder_id STRING(MAX) NOT NULL, -- The actor
    action_type STRING(MAX),
    timestamp TIMESTAMP OPTIONS (allow_commit_timestamp=true),
) PRIMARY KEY (log_id);


CREATE OR REPLACE PROPERTY GRAPH FloodPulseGraph
  NODE TABLES (Nodes PROPERTIES (node_id, name, type, status, flash_risk_index, elevation))
  EDGE TABLES (Edges SOURCE KEY (source_node_id) REFERENCES Nodes (node_id)
               DESTINATION KEY (dest_node_id) REFERENCES Nodes (node_id)
               LABEL Connects PROPERTIES (current_weight, is_flood_prone));