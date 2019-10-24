from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication


class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        user = cache.get(token)
        return user, token
