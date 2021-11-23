from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def CantidadMayorCeroValidador(value):
    if value <=0:
        raise ValidationError(
            ('La cantidad debe ser mayor a 0'),
            params={'value':value}
        )