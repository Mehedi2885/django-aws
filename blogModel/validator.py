from django.core.exceptions import ValidationError


def valid_mehedi(value):
    if 'mehedi' in value:
        return value
    else:
        raise ValidationError('This is not mehedi')
