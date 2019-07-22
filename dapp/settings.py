from django.conf import settings

SETTINGS = getattr(settings, 'DAPP_SETTINGS',
                   {
                       'NODE_URL': 'http://localhost:8545',
                       'IS_POA': False,
                   })

NODE_URL = SETTINGS['NODE_URL']
IS_POA = SETTINGS['IS_POA']