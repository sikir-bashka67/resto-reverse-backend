from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from clients.models import Client

User = get_user_model()


class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
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
        fields = ['id', 'name', 'email', 'phone', 'created_at', 'password']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        val = (value or '').strip()
        if not val:
            raise serializers.ValidationError('Имя клиента не может быть пустым.')
        return val

    def validate_password(self, value):
        if value and len(value) < 8:
            raise serializers.ValidationError('Пароль не может быть длиной менее 8 символов.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=password or User.objects.make_random_password()
        )
        return Client.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.user.set_password(password)
            instance.user.save()

        if 'name' in validated_data:
            validated_data['name'] = validated_data['name'].strip()

        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name', 'phone']

    def create(self, validated_data):
        client_name = validated_data.pop('name')
        client_phone = validated_data.pop('phone')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

        Client.objects.create(
            user=user,
            name=client_name,
            phone=client_phone,
            email=user.email
        )

        return user