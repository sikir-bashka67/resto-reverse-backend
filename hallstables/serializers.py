from rest_framework import serializers
from hallstables.models import Hall, Table

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ['id', 'name', 'width', 'height', 'created_at']

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'