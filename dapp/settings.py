from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

NODE_URL = getattr(settings, 'DAPP_NODE_URL', None)
IS_POA = getattr(settings, 'DAPP_IS_POA', False)

if NODE_URL is None:
    raise ImproperlyConfigured('NODE_URL is not set')

