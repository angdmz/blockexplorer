from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from dapp import settings
from .gateway import Gateway, HTTPProviderGenerator

generator = HTTPProviderGenerator()
generator.url = settings.NODE_URL
is_poa = settings.IS_POA

def validate_address(value):
    gateway = Gateway(generator, is_poa)
    if not gateway.is_valid_address(value):
        raise ValidationError(_('%(value)s is not a valid address'), params={'value': value})