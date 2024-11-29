from rest_framework import serializers

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