from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


"""POR TERMINAR """
def ValidadorPagaCon(value,pedido):
    
    if value :
        raise ValidationError(
            ('%(value)s no es un número negativo'),
            params={'value':value}
        )
