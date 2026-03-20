from ninja.security import HttpBearer
from django.contrib.auth.models import User
from django.db import models


if not hasattr(User, "auth_token"):
    User.add_to_class("auth_token", models.CharField(max_length=64, blank=True, null=True))

class SimpleBearerAuth(HttpBearer):
    def authenticate(self, request, token: str):
        try:
            return User.objects.get(auth_token=token)
        except User.DoesNotExist:
            return None