# Register your models here.
from datetime import datetime

from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from django.contrib.postgres import fields as postgresfields

from ethereum.models import Account, Block, TransactionRelationship, SmartContract, ABI


class TransactionRelationshipAdmin(admin.ModelAdmin):
    fields = ('hash', 'from_account', 'to_account', 'nonce', 'block_number', 'block_miner', 'block_date')
    readonly_fields = ('hash', 'from_account', 'to_account', 'nonce', 'block_number', 'block_miner', 'block_date')


class SmartContractAdmin(admin.ModelAdmin):
    fields = ('abi', 'abi_text', 'deploy_tx', 'deployer')
    readonly_fields = ('abi_text', 'deploy_tx', 'deployer')


class ABIAdmin(admin.ModelAdmin):
    fields = ('json', 'label')
    formfield_overrides = {
        postgresfields.JSONField: {'widget': JSONEditorWidget}
    }


admin.site.register(Account)
admin.site.register(TransactionRelationship, TransactionRelationshipAdmin)
admin.site.register(Block)
admin.site.register(SmartContract, SmartContractAdmin)
admin.site.register(ABI, ABIAdmin)
