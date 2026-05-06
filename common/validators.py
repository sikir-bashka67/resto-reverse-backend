import re
from django.core.exceptions import ValidationError


def validate_phone(value):
    if not re.match(r'^\+?[\d\s\-]{7,15}$', value):
        raise ValidationError("Неверный формат номера телефона.")