from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from rest_framework import serializers

from staff.models import Staff


class StaffSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?\d{9,15}$',
                message="Телефон должен содержать только цифры и может начинаться с '+'.",
            )
        ]
    )

    class Meta:
        model = Staff
        fields = ['id', 'username', 'name', 'role', 'email', 'phone', 'password', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'phone': {'required': True},
            'created_at': {'read_only': True},
        }

    def validate_name(self, value):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('Имя сотрудника не может быть пустым.')
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Пароль должен содержать не менее 8 символов.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        return Staff.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        if 'name' in validated_data:
            validated_data['name'] = validated_data['name'].strip()
        return super().update(instance, validated_data)
