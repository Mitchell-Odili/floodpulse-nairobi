# level_3/models/mission.py
from pydantic import BaseModel, Field
from typing import List

class RescuePlan(BaseModel):
    priority_node_id: str
    responder_id: str = Field(description="The assigned unit/personnel for this node")
    route_path: List[str] = Field(description="Sequence of node_ids to travel through")
    estimated_arrival: str = Field(description="Estimated time based on edge weights")