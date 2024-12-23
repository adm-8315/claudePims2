from datetime import datetime, timedelta
import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from core.models.users import User

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            # Get the token from header
            token = auth_header.split(' ')[1]
            # Decode the token
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )

            # Get user from payload
            user = User.objects.filter(id=payload['user_id']).first()
            if not user:
                raise AuthenticationFailed('User not found')

            if not user.active:
                raise AuthenticationFailed('User is inactive')

            return (user, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except Exception as e:
            raise AuthenticationFailed(str(e))

    @staticmethod
    def generate_token(user):
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm='HS256'
        )
