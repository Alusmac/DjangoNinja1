from ninja.security import HttpBearer
from django.contrib.auth.models import User

class SimpleBearerAuth(HttpBearer):
    def authenticate(self, request, token):
        print("TOKEN RECEIVED:", token)
        try:
            user = User.objects.get(username=token)
            print("USER FOUND:", user)
            return user
        except User.DoesNotExist:
            print("USER NOT FOUND")
            return None