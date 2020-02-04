from django.db import models

from ethereum.managers import TransactionManager, BlockManager


class Receipt(models.Model):
    cumulative_gas_used = models.IntegerField(null=True)
    gas_used = models.IntegerField(null=True)
    status = models.IntegerField(null=True)
    transaction_hash = models.CharField(max_length=82, unique=True, null=True)

    def __str__(self):
        return "Hash: {} - gas: {}".format(str(self.transaction_hash), str(self.gas_used))


class Account(models.Model):
    public_key = models.CharField(max_length=42, null=True)
    balance_in_wei = models.CharField(max_length=50, db_column='balance_in_wei', default='0', null=True)

    def __str__(self):
        return self.public_key

    class Meta:
        db_table = 'accounts'


class Block(models.Model):
    timestamp = models.BigIntegerField(null=True)
    number = models.IntegerField(null=True, db_index=True)
    hash = models.CharField(max_length=66, null=True)
    mix_hash = models.CharField(null=True, max_length=66)
    difficulty = models.BigIntegerField(null=True)
    gas_limit = models.IntegerField(null=True)
    gas_used = models.IntegerField(null=True)
    state_root = models.CharField(null=True, max_length=66)
    receipts_root = models.CharField(null=True, max_length=66)
    transactions_root = models.CharField(null=True, max_length=66)
    total_difficulty = models.BigIntegerField(null=True)
    size = models.BigIntegerField(null=True)
    nonce = models.CharField(max_length=50, null=True)
    parent_hash = models.CharField(max_length=66, null=True)
    miner = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    sha3_uncles = models.CharField(null=True, max_length=66)
    objects = BlockManager()

    def __str__(self):
        return "Blk N° : {}".format(str(self.number))

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

    def __str__(self):
        return "Hash: {} - gas: {}".format(str(self.hash), str(self.gas))

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


class TransactionRelationship(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='from_account', null=True)
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_account', null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'Tx : {}; from : {}; to : {}; block : {}; receipt : {}'

    class Meta:
        db_table = 'transaction_relationships'
        unique_together = ('from_account', 'to_account', 'transaction')
        verbose_name = 'TX - Account relation'
        verbose_name_plural = 'TX - Account relations'
