from rest_framework import serializers
from .models import Users
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        label="Confirm Password",
    )

    class Meta:
        model = Users
        fields = [
            "user_id",
            "user_name",
            "email",
            "password",
            "password2",
            "name",
            "last_name",
            "phone",
            "curp",
            "rfc",
            "birth_date",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
            "user_id": {"read_only": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "The passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = Users.objects.create_user(**validated_data)
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
            "name",
            "last_name",
            "phone",
            "curp",
            "rfc",
            "birth_date",
            "password",
        ]

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
