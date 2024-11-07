from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from fintrackr.core.models import Users

class UserSerializer(serializers.ModelSerializer):
    password_hash = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['user_name', 'email', 'name', 'last_name', 'phone', 'curp', 'rfc', 'birth_date', 'password_hash']

    def create(self, validated_data):
        validated_data['password_hash'] = make_password(validated_data['password_hash'])
        return Users.objects.create(**validated_data)
