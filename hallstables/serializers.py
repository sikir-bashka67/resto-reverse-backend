from rest_framework import serializers
from hallstables.models import Hall, Table


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'

    def validate(self, data):
        width = data.get('width') if 'width' in data else (self.instance.width if self.instance else None)
        height = data.get('height') if 'height' in data else (self.instance.height if self.instance else None)

        if (width is not None and width <= 0) or (height is not None and height <= 0):
            raise serializers.ValidationError({'size': 'Размеры зала должны быть больше 0.'})
        return data


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

    def validate(self, data):
        seats = data.get('seats')
        if seats is not None and seats <= 0:
            raise serializers.ValidationError({'seats': 'Количество мест должно быть положительным числом.'})

        hall = data.get('hall') or (self.instance.hall if self.instance else None)
        x = data.get('x') if 'x' in data else (self.instance.x if self.instance else None)
        y = data.get('y') if 'y' in data else (self.instance.y if self.instance else None)

        if hall and x is not None and y is not None:
            if x < 0 or x > hall.width or y < 0 or y > hall.height:
                raise serializers.ValidationError({'cords': 'Координаты должны находиться в пределах размеров зала.'})

        return data