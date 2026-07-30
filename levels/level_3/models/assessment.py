from pydantic import BaseModel, Field
from typing import List, Optional

class NodeTelemetry(BaseModel):
    node_id: str = Field(description="Unique identifier of the node (e.g., node_001)")
    name: str = Field(description="Entity or location name (e.g., Sarah)")
    node_type: str = Field(description="Type of node: Resident, Responder, or Infrastructure")
    lat: float = Field(description="Latitude coordinate")
    lon: float = Field(description="Longitude coordinate")
    elevation_m: float = Field(description="Elevation in meters")
    risk_level: str = Field(description="Classified risk level from database status")
    flash_risk_index: float = Field(description="Numeric flash flood risk index on a 0.0 to 1.0 scale")


class BasinAssessment(BaseModel):
    overall_status: str = Field(description="Summary: SAFE, WARNING, or CRITICAL")
    reason: str = Field(description="Concise justification based on simulation")
    critical_nodes: List[NodeTelemetry] = Field(description="List of nodes currently experiencing high risk or Critical Pulse across the basin")
    matching_nodes: Optional[List[NodeTelemetry]] = Field(
        default=None, 
        description="Specific records found when searching for a targeted entity name (e.g., looking up 'Sarah')"
    )
    resident_impact_summary: str = Field(description="Description of the demographic or location-specific risk for these nodes")