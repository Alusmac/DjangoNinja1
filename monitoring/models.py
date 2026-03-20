from django.db import models
from django.contrib.auth.models import User


class Server(models.Model):
    """Server information
    """
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Metric(models.Model):
    """Metric information
    """
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="metrics")
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    disk_usage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.server.name} - {self.created_at}"
