from rest_framework import serializers
from Register_Login.models import Profile, Notification_token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification_token
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=("password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )
