from pydantic import BaseModel
from typing import List, Dict

class Node(BaseModel):
    id: str
    label: str
    size: int # Represents frequency of the activity

class Edge(BaseModel):
    source: str
    target: str
    weight: int # Represents frequency of the transition

class ProcessModel(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
