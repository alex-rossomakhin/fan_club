from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('Год %(value)s больше текущего!'),
            params={'value': value},
        )


def validate_username(value):
    if 'me' == value:
        raise ValidationError(
            ('Имя пользователя не может быть <me>.'),
            params={'value': value},
        )
