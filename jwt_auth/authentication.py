from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.conf import settings  # show secret key in settings.py
import jwt

User = get_user_model()


class JWTAuthentication(BasicAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')

        # Check if it has a header
        if not header:
            return None

        # Checks correct token format
        if not header.startswith('Bearer'):
            raise PermissionDenied(detail='Invalid Auth Token')

        token = header.replace("Bearer", "")

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithm=['HS256'])
            user = User.objects.get(pk=payload.get('sub'))
            print('USER ->', user)
        
        #if we get an error from the try section 
        except jwt.exceptions.InvalidTokenError:
            raise PermissionDenied(detail='Invalid Token')
        
        
        # If the user does not exist it will fall into the below
        except User.DoesNotExist:
            raise PermissionDenied(detail='User Not Found')

        # if all good, return user and the token
        return (user, token)
