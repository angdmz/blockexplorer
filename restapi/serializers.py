from rest_framework import serializers
from ethereum.models import Account, Block, TransactionRelationship


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('number', 'hash', 'mix_hash', 'timestamp', 'difficulty', 'gas_limit', 'gas_used', 'state_root',
                  'receipt_root', 'transactions_root', 'total_difficulty', 'size', )


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'public_key')


class TransactionSerializer(serializers.ModelSerializer):
    hash = serializers.SerializerMethodField()
    block_number = serializers.SerializerMethodField()
    gas = serializers.SerializerMethodField()
    gas_price = serializers.SerializerMethodField()
    input = serializers.SerializerMethodField()
    from_account = serializers.SerializerMethodField()
    to_account = serializers.SerializerMethodField()
    cumulative_gas_used = serializers.SerializerMethodField()
    gas_used = serializers.SerializerMethodField()
    nonce = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    def get_hash(self, obj):
        tx_hash = obj.transaction.hash if obj.transaction is not None else None
        return tx_hash

    def get_block_number(self, obj):
        block_number = obj.block.number if obj.block is not None else None
        return block_number

    def get_gas(self, obj):
        gas = obj.transaction.gas if obj.transaction is not None else None
        return gas

    def get_gas_price(self, obj):
        gas_price = obj.transaction.gas_price if obj.transaction is not None else None
        return gas_price

    def get_input(self, obj):
        tx_input = obj.transaction.input if obj.transaction is not None else None
        return tx_input

    def get_from_account(self, obj):
        from_account = obj.transaction.from_account if obj.transaction is not None else None
        return from_account

    def get_to_account(self, obj):
        to_account = obj.transaction.to_account if obj.transaction is not None else None
        return to_account

    def get_cumulative_gas_used(self, obj):
        cumulative_gas_used = obj.receipt.cumulative_gas_used if obj.receipt is not None else None
        return cumulative_gas_used

    def get_gas_used(self, obj):
        gas_used = obj.receipt.gas_used if obj.receipt is not None else None
        return gas_used

    def get_nonce(self, obj):
        nonce = obj.transaction.nonce if obj.transaction is not None else None
        return nonce

    def get_value(self, obj):
        value = obj.transaction.value if obj.transaction is not None else None
        return value

    class Meta:
        model = TransactionRelationship
        fields = ('hash', 'gas', 'gas_price', 'input',
                  'from_account', 'to_account', 'cumulative_gas_used', 'gas_used', 'nonce', 'value', 'block_number', )
