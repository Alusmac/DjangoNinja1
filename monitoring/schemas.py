from pydantic import BaseModel
from datetime import datetime


class ServerIn(BaseModel):
    """Server information
    """
    name: str
    ip_address: str
    status: bool = True


class ServerOut(BaseModel):
    """Server out put information
    """
    id: int
    name: str
    ip_address: str
    status: bool
    created_at: datetime


class MetricIn(BaseModel):
    """Metric information
    """
    server_id: int
    cpu_usage: float
    memory_usage: float
    disk_usage: float


class MetricOut(BaseModel):
    """Metric out put information
    """
    id: int
    server_id: int
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    created_at: datetime
