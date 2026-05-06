from rest_framework import serializers
from menuorderspreorders.models import Menu, Category, Profile, PreOrder, OrderItem, Order, PreOrderItem
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Menu
        fields = ['id', 'name', 'price', 'category', 'description']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше 0")
        return value

    def validate_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Название категории или блюда не может быть пустым")
        return value


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'phone', 'birth_date']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        profile = super().update(instance, validated_data)
        if user_data:
            user = instance.user
            user.email = user_data.get('email', user.email)
            user.save()

        return profile


class PreOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreOrder
        fields = '__all__'


class PreOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreOrderItem
        fields = '__all__'

    def validate(self, data):
        if data.get('quantity', 0) <= 0:
            raise serializers.ValidationError({"quantity": "Количество должно быть больше 0"})
        if data.get('price_at_ordering_time', 0) <= 0:
            raise serializers.ValidationError({"price_at_ordering_time": "Цена должна быть больше 0"})
        return data


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def validate(self, data):
        if data.get('quantity', 0) <= 0:
            raise serializers.ValidationError({"quantity": "Количество должно быть больше 0"})
        if data.get('price_at_ordering_time', 0) <= 0:
            raise serializers.ValidationError({"price_at_ordering_time": "Цена должна быть больше 0"})
        return data