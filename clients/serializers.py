from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from clients.models import Client

User = get_user_model()


class ClientSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?\d{9,15}$',
                message="Телефон должен содержать только цифры и может начинаться с '+'.",
            )
        ]
    )

    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone', 'password', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
        }

    def validate_name(self, value):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('Имя клиента не может быть пустым.')
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Пароль должен содержать не менее 8 символов.')
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
        if 'name' in validated_data:
            validated_data['name'] = validated_data['name'].strip()
        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user