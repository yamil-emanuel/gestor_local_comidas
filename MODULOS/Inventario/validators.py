from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def ValorPromocionValidador(value):
    if value >0:
        raise ValidationError(
            ('%(value)s no es un número negativo'),
            params={'value':value}
        )

