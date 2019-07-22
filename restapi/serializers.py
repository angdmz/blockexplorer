from rest_framework import serializers
from ethereum.models import Account, Transaction, Block, TransactionRelationship


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
    receipt = serializers.SerializerMethodField()
    from_account = serializers.SerializerMethodField()
    to_account = serializers.SerializerMethodField()

    def get_hash(self, obj):
        tx = obj.get_transaction()
        codigo = tx.hash
        return codigo

    def get_asignacion_nombre(self, obj):
        asignacion = obj.get_asignacion()
        descripcion = asignacion.cod_estructura_desempenio.descripcion if asignacion is not None else None
        return descripcion

    def get_en_proceso_baja(self, obj):
        en_proceso_baja = obj.get_en_proceso_baja()
        return en_proceso_baja

    def get_cod_convenio(self, obj):
        asignacion = obj.get_asignacion()
        cod_convenio = asignacion.cod_convenio.cod_convenio if asignacion is not None else None
        return cod_convenio

    def get_convenio_descripcion(self, obj):
        asignacion = obj.get_asignacion()
        descripcion = asignacion.cod_convenio.descripcion if asignacion is not None else None
        return descripcion

    class Meta:
        model = TransactionRelationship
        fields = ('transaction__hash', 'transaction__gas', 'transaction__gas_price', 'transaction__input',
                  'transaction__transaction_index', 'transaction__nonce', 'transaction__value')
