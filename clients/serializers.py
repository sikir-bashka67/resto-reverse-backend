from rest_framework import serializers
from clients.models import Client
from common.validators import validate_phone
from django.contrib.auth.hashers import make_password


class ClientSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[validate_phone])

    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone', 'password', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True}
        }

    def validate_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Имя не может быть пустым.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.password = make_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        return super().update(instance, validated_data)