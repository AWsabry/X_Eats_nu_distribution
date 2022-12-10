from rest_framework import serializers
from Register_Login.models import Profile
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=_("password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )

    def clean(self,*args,**kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(email = email, password=password)
        if not user:
            raise serializers.ValidationError("This user does not exist")
        if not user.check_password(password):
            raise serializers.ValidationError("Password is incorrect")
        if not user.is_active:
            raise serializers.ValidationError("This user is not active, check Your inbox or make sure you logged in with valid email")
        return super(LoginSerializer,self).clean(*args,**kwargs)
