from rest_framework import serializers
from fintrackr.core.models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            "user_name",
            "email",
            "name",
            "last_name",
            "phone",
            "curp",
            "rfc",
            "birth_date",
            "password_hash",
        ]

    def update(self, instance, validated_data):
        instance.user_name = validated_data.get("user_name", instance.user_name)
        instance.email = validated_data.get("email", instance.email)
        instance.name = validated_data.get("name", instance.name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.curp = validated_data.get("curp", instance.curp)
        instance.rfc = validated_data.get("rfc", instance.rfc)
        instance.birth_date = validated_data.get("birth_date", instance.birth_date)

        password_hash = validated_data.get("password_hash")
        if password_hash:
            instance.set_password(password_hash)

        instance.save()
        return instance
