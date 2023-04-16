from django.core.exceptions import ValidationError


def validate_username(value):
    '''Валидатор что имя не создано из me'''
    if value == 'me':
        raise ValidationError(
            ('Логин не может быть <me>.'),
            params={'value': value},
        )