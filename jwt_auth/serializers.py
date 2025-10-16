from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate(self, data):
        print('Data', data)

        password = data.pop('password')
        password_confirmation = data.pop('password_confirmation')

        # check if they match
        if password != password_confirmation:
            raise ValidationError({'password_confirmation': 'do not match'})

        # check if password valid
        try:
            password_validation.validate_password(password=password)
        except ValidationError as error:
            print('VALIDATION ERROR')
            raise ValidationError({'password': error.message})

        # hash password
        data['password'] = make_password(password)

        print('DATA -> ', data)
        return data

    # ST: Updated Meta fields to return only necessary data
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'profile_image', 'password', 'password_confirmation')
