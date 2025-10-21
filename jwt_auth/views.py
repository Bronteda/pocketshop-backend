from rest_framework.views import APIView # main API controller class
from rest_framework.response import Response #response class
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from datetime import datetime, timedelta # creates timestamps in dif formats
from django.contrib.auth import get_user_model # gets user model we are using
from django.conf import settings # import our settings for our secret
from .serializers import UserSerializer
import jwt # import jwt

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        print('User created: ', user_to_create)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_202_ACCEPTED)
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username') if request.data.get('username') is not None else None
        email = request.data.get('email') if request.data.get('email') is not None else None
        password = request.data.get('password')

        try:
            if ( username is not None and email is None):
                user_to_login = User.objects.get(username=username)
                
            elif ( email is not None and username is None):   
                user_to_login = User.objects.get(email=email)
                
        except User.DoesNotExist:
            raise PermissionDenied(detail='Invalid Credentials')
        
        if not user_to_login.check_password(password):
            raise PermissionDenied( detail= 'Invalid Credentials')
        
        # ST: Updated payload to include user data when sending to client
        
        dt = datetime.now() + timedelta(days=7) # validity of token
        payload = {
            'sub': str(user_to_login.id),
            'id': user_to_login.id,
            'username': user_to_login.username,
            'email': user_to_login.email,
            'first_name': user_to_login.first_name,
            'last_name': user_to_login.last_name,
            'exp': int(dt.strftime('%s'))
        }
        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        return Response({ 'token': token })