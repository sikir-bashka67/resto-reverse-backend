from rest_framework import serializers
from clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = ['name', 'email', 'password']

    def create(self, validated_data):
        client = Client.objects.create(name=validated_data['name'], email=validated_data['email'], password=validated_data['password'])
        return client

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)