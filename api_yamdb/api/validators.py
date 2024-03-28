from django.core.exceptions import ValidationError


def validate_username(value):
    if 'me' == value:
        raise ValidationError(
            ('Имя пользователя не может быть <me>.'),
            params={'value': value},
        )
