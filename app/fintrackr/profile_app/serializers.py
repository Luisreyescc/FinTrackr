from rest_framework import serializers
from fintrackr.core.models import Users

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_name', 'email', 'name', 'last_name', 'phone', 'curp', 'rfc', 'birth_date']  # Solo los campos que el usuario puede editar

    def update(self, instance, validated_data):
        """Actualiza los campos de la instancia de usuario, ignorando campos vacíos."""
        for attr, value in validated_data.items():
            if value != "":
                setattr(instance, attr, value)
        instance.save()
        return instance
