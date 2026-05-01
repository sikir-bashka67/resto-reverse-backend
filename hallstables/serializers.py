from rest_framework import serializers
from hallstables.models import Hall, Table


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'

    def validate(self, data):
        if data.get('x', 0) <= 0 or data.get('y', 0) <= 0:
            raise serializers.ValidationError("Размеры зала должны быть больше 0.")
        return data


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

    def validate(self, data):
        seats = data.get('seats')
        if seats is not None and seats <= 0:
            raise serializers.ValidationError({"seats": "Вместимость должна быть положительным числом"})

        hall = data.get('hall') or (self.instance.hall if self.instance else None)
        x = data.get('x') if 'x' in data else (self.instance.x if self.instance else None)
        y = data.get('y') if 'y' in data else (self.instance.y if self.instance else None)

        if hall and x is not None and y is not None:
            if x < 0 or x > hall.x or y < 0 or y > hall.y:
                raise serializers.ValidationError("Координаты (x, y) выходят за пределы размеров зала")

        return data