from django.db import models

class Account(models.Model):
    public_key = models.CharField(max_length=42)
    balance = models.IntegerField

    class Meta:
        db_table = 'accounts'

class Transaction(models.Model):
    tx_hash = models.CharField(max_length=82)
    gas_price = models.IntegerField
    gas = models.IntegerField
    block_number = models.IntegerField
    timestamp = models.TimeField

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

class AccountTransactionRelation(models.Model):
    from_account = models.ForeignKey(Account,on_delete=models.CASCADE, related_name='from_account')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_account')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    class Meta:
        db_table = 'account_transaction'