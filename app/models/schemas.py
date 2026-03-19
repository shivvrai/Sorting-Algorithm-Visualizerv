"""Pydantic request / response models for input validation."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class SortRequest(BaseModel):
    array: List[int] = Field(..., min_length=1, max_length=500, description="Array to sort")
    algorithm: str = Field(default="bubble", description="Sorting algorithm name")


class GraphSolveRequest(BaseModel):
    graph: Dict[str, Dict[str, Any]] = Field(..., description="Adjacency list")
    algorithm: str = Field(default="bfs", description="Graph algorithm name")
    start: str = Field(..., description="Start node label")
    directed: bool = Field(default=False)
    target: Optional[str] = Field(default=None, description="Target node (Dijkstra)")


class TimeTrialRequest(BaseModel):
    array: List[int] = Field(..., min_length=1, max_length=500, description="Array for time trial")


class ExportRequest(BaseModel):
    format: str = Field(default="json", description="Export format: json or csv")
    results: Dict[str, Any] = Field(default_factory=dict)
