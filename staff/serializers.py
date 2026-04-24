from rest_framework import serializers
from staff.models import Staff


class StaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Staff
        fields = ['id', 'name', 'role', 'email', 'phone', 'password', 'created_at']

    def create(self, validated_data):
        return Staff.objects.create_user(**validated_data)