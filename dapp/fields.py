from django.db.models.fields import CharField
from dapp.validators import validate_address


class AddressField(CharField):
    def __init__(self, *args, **kwargs):
        self.default_validators.append(validate_address)
        super().__init__(*args, **kwargs)
