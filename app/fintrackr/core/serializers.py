from rest_framework import serializers
from .models import Users
from django.contrib.auth import authenticate


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "username", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ["user_name", "email", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = Users.objects.create_user(
            user_name=validated_data["user_name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    def validate(self, attrs):
        user = authenticate(username=attrs["user_name"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError({"detail": "Invalid credentials.."})
        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            "user_id",
            "user_name",
            "email",
            "name",
            "last_name",
            "phone",
            "curp",
            "rfc",
            "birth_date",
        ]
        read_only_fields = ["user_id", "user_name", "email"]


class UpdateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=False, style={"input_type": "password"}
    )

    class Meta:
        model = Users
        fields = [
            "user_name",
            "name",
            "last_name",
            "email",
            "phone",
            "curp",
            "rfc",
            "birth_date",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
