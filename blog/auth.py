from ninja.security import HttpBearer
from django.contrib.auth.models import User


class SimpleBearerAuth(HttpBearer):
    def authenticate(self, request, token) -> User | None:
        """ Authenticate user
        """
        try:
            user = User.objects.get(username=token)
            return user
        except User.DoesNotExist:
            return None
