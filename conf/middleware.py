from rest_framework_simplejwt.authentication import JWTAuthentication

from conf import settings
from user.models import User


class DebugModeAuthentication(JWTAuthentication):

    def _user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass

    def authenticate(self, request):
        user_id = request.headers.get('X-User-Id', None)
        if settings.DEBUG is True and user_id:
            user = self._user(user_id)
            if user:
                return user, f"Token {user_id}"
        return super(DebugModeAuthentication, self).authenticate(request)
