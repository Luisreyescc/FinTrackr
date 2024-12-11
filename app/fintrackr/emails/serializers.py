from rest_framework import serializers
from core.models import Users

class SendCodeSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True)

class ValidateCodeSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=255, required=True)
    recovery_code = serializers.CharField(max_length=6, required=True)

class ChangePasswordSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    admin_user = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = Users
        fields = ["user_name", "email", "password", "password2", "admin_user"]
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        admin_user = validated_data.pop("admin_user", False)
        user = Users.objects.create_user(
            user_name=validated_data["user_name"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_staff=admin_user
        )
        return user