from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import CustomUser


class UserRegistrationSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email"]

    def create(self, validated_data) -> CustomUser:
        return CustomUser.objects.create_user(**validated_data)
