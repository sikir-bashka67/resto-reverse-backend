from django.utils import timezone
from rest_framework import serializers
from menuorderspreorders.models import Category, Menu, Order, OrderItem, PreOrder, PreOrderItem, Profile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Menu
        fields = ['id', 'name', 'price', 'category', 'description', 'is_available', 'created_at']
        read_only_fields = ['created_at']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Цена не может быть ниже нуля.')
        return value

    def validate_name(self, value):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('Название не может быть пустым.')
        return value


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'email', 'bio', 'location', 'birth_date']
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def validate_birth_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError('Дата рождения не может быть в будущем.')
        return value


class PreOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreOrder
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }


class PreOrderItemSerializer(serializers.ModelSerializer):
    price_at_ordering_time = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = PreOrderItem
        fields = '__all__'

    def validate(self, data):
        if data.get('quantity', 0) <= 0:
            raise serializers.ValidationError({'quantity': 'Количество должно быть больше 0.'})
        return data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }


class OrderItemSerializer(serializers.ModelSerializer):
    price_at_ordering_time = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'

    def validate(self, data):
        if data.get('quantity', 0) <= 0:
            raise serializers.ValidationError('Количество должно быть больше 0.')
        return data