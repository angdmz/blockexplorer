# Register your models here.

from django.contrib import admin
from ethereum.models import Account, Transaction, Block

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Block)
