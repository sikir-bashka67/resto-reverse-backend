from rest_framework import serializers
from menuorderspreorders.models import Menu, Category, Profile, PreOrder, OrderItem, Order, PreOrderItem
from django.utils import timezone


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

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


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'email', 'bio', 'location', 'birth_date']

    def validate_birth_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError(
                "Дата рождения не может быть в будущем"
            )
        return value

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        new_email = user_data.get('email')

        if new_email and instance.user:
            instance.user.email = new_email
            instance.user.save()

        return super().update(instance, validated_data)


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
        if data.get('price_at_order_time', 0) <= 0:
            raise serializers.ValidationError({"price_at_order_time": "Цена должна быть больше 0"})
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
        if data.get('price_at_order_time', 0) <= 0:
            raise serializers.ValidationError({"price_at_order_time": "Цена должна быть больше 0"})
        return data