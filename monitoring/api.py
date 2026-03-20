from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Server, Metric
from .schemas import ServerIn, ServerOut, MetricIn, MetricOut
from .auth import SimpleBearerAuth

router = Router()
auth_scheme = SimpleBearerAuth()


def server_to_out(server: Server) -> ServerOut:
    """Server to output
     """
    return ServerOut(
        id=server.id,
        name=server.name,
        ip_address=server.ip_address,
        status=server.status,
        created_at=server.created_at
    )


def metric_to_out(metric: Metric) -> MetricOut:
    """Metric to output
    """
    return MetricOut(
        id=metric.id,
        server_id=metric.server.id,
        cpu_usage=metric.cpu_usage,
        memory_usage=metric.memory_usage,
        disk_usage=metric.disk_usage,
        created_at=metric.created_at
    )


@router.post("/servers/", response=ServerOut, auth=auth_scheme)
def create_server(request, data: ServerIn) -> ServerOut:
    """Create server
    """
    server = Server.objects.create(**data.dict())
    return server_to_out(server)


@router.get("/servers/", response=List[ServerOut], auth=auth_scheme)
def list_servers(request) -> List[ServerOut]:
    """List servers
    """
    return [server_to_out(s) for s in Server.objects.all()]


@router.get("/servers/{server_id}/", response=ServerOut, auth=auth_scheme)
def get_server(request, server_id: int) -> ServerOut:
    """Get server
    """
    server = get_object_or_404(Server, id=server_id)
    return server_to_out(server)


@router.put("/servers/{server_id}/", response=ServerOut, auth=auth_scheme)
def update_server(request, server_id: int, data: ServerIn) -> ServerOut:
    """Update server
    """
    server = get_object_or_404(Server, id=server_id)
    for attr, value in data.dict().items():
        setattr(server, attr, value)
    server.save()
    return server_to_out(server)


@router.delete("/servers/{server_id}/", auth=auth_scheme)
def delete_server(request, server_id: int) -> ServerOut:
    """Delete server
    """
    server = get_object_or_404(Server, id=server_id)
    server.delete()
    return {"success": True}


@router.post("/metrics/", response=MetricOut, auth=auth_scheme)
def add_metric(request, data: MetricIn) -> MetricOut:
    """Add metric
    """
    metric = Metric.objects.create(
        server_id=data.server_id,
        cpu_usage=data.cpu_usage,
        memory_usage=data.memory_usage,
        disk_usage=data.disk_usage
    )

    alerts = []
    if metric.cpu_usage > 90:
        alerts.append("CPU usage > 90%")
    if metric.memory_usage > 90:
        alerts.append("Memory usage > 90%")
    if metric.disk_usage > 90:
        alerts.append("Disk usage > 90%")
    if alerts:
        print(f"ALERT for server {metric.server.name}: {', '.join(alerts)}")
    return metric_to_out(metric)


@router.get("/servers/{server_id}/metrics/", response=List[MetricOut], auth=auth_scheme)
def list_metrics(request, server_id: int) -> List[MetricOut]:
    """List metrics
    """
    metrics = Metric.objects.filter(server_id=server_id)
    return [metric_to_out(m) for m in metrics]
