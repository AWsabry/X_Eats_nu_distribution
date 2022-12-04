from rest_framework import serializers
from Register_Login.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['email',"first_name", "last_name", 'is_active',
                    "is_staff","is_superuser","title","PhoneNumber","last_modified","Wallet","is_operation",]


