from django.db import models

from synchro.managers import TransactionManager, BlockManager


class Receipt(models.Model):
    cumulative_gas_used = models.IntegerField

class Account(models.Model):
    public_key = models.CharField(max_length=42, null=True)
    balance_in_gwei = models.BigIntegerField(db_column='balance_in_gwei', default=0, null=True)

    class Meta:
        db_table = 'accounts'

class Block(models.Model):
    timestamp = models.DateTimeField(null=True)
    number = models.IntegerField(null=True, db_index=True)
    hash = models.CharField(max_length=80, null=True)
    mix_hash = models.CharField(null=True, max_length=50)
    difficulty = models.BigIntegerField(null=True)
    gas_limit = models.IntegerField(null=True)
    gas_used = models.IntegerField(null=True)
    state_root = models.CharField(null=True, max_length=50)
    receipt_root = models.CharField(null=True, max_length=50)
    transactions_root = models.CharField(null=True, max_length=50)
    total_difficulty = models.BigIntegerField(null=True)
    size = models.IntegerField(null=True)
    objects = BlockManager()

    class Meta:
        db_table = 'blocks'
        verbose_name_plural = 'Blocks'
        verbose_name = 'Block'
        unique_together = ('hash', 'number', )

class Transaction(models.Model):
    hash = models.CharField(max_length=82, unique=True, null=True)
    gas_price = models.BigIntegerField(null=True)
    gas = models.IntegerField(null=True)
    input = models.TextField(null=True)
    transaction_index = models.IntegerField(null=True)
    nonce = models.IntegerField(null=True)
    value = models.BigIntegerField(null=True)
    objects = TransactionManager()

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


class TransactionRelationship(models.Model):
    from_account = models.ForeignKey(Account,on_delete=models.CASCADE, related_name='from_account', null=True)
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_account', null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'transaction_relationships'
        unique_together = ('from_account', 'to_account', 'transaction')
        verbose_name = 'TX - Account relation'
        verbose_name_plural = 'TX - Account relations'
