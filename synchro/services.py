import datetime

from django.db import transaction

from dapp.gateway import Gateway, HTTPProviderGenerator
from ethereum.models import Transaction, Block, Account, TransactionRelationship


class TransactionSynchro:
    gateway = Gateway(HTTPProviderGenerator())
    tx_manager = Transaction.objects
    def sync_tx(self, tx):
        tx_model, created = self.tx_manager.update_or_create(
                                                hash=tx['hash'],
                                                defaults=
                                                {
                                                    'gas': tx['gas'],
                                                    'gas_price': tx['gasPrice'],
                                                    'input': tx['input'],
                                                    'value': tx['value'],
                                                    'transaction_index': tx['transactionIndex'],
                                                    'nonce':tx['nonce']}
                                                )
        return tx_model, created


class BlockSynchro:

    blk_manager = Block.objects

    def sync_block(self, block):
        tx_model, created = self.blk_manager.update_or_create(
            hash=block['hash'],
            defaults=
            {
                'gas_used': block['gasUsed'],
                'gas_limit': block['gasLimit'],
                'number': block['number'],
                'timestamp': datetime.datetime.fromtimestamp(block['timestamp']),
                'size': block['size']
            }
        )
        return tx_model, created


class ReceiptSynchro:

    rpt_manager = Block.objects

    def sync_receipt(self, block):
        rpt_manager, created = self.rpt_manager.update_or_create(
            hash=block['hash'],
            defaults=
            {
                'cumulative_gas_used': block['gasUsed'],
            }
        )
        return rpt_manager, created


class AccountSynchro:

    acc_manager = Account.objects

    def sync_account(self, address):
        acc_model, created = self.acc_manager.update_or_create(public_key=address)
        return acc_model, created


class TransactionRelationSynchro:

    txrel_manager = TransactionRelationship.objects

    def syn_txrel(self, tx, **options):
        return self.txrel_manager.update_or_create(transaction=tx, defaults=options)


class BlockProcess:

    gateway = Gateway(HTTPProviderGenerator())
    blk_synchro = BlockSynchro()
    rpt_synchro = ReceiptSynchro()
    tx_synchro = TransactionSynchro()
    acc_synchro = AccountSynchro()
    txrel_synchro = TransactionRelationSynchro()

    def process(self, block_number):
        block = self.gateway.get_block(block_number)
        with transaction.atomic():
            block_obj, created = self.blk_synchro.sync_block(block)
            for tx in block['transactions']:
                receipt = self.gateway.get_tx_receipt(tx)
                full_tx = self.gateway.get_transaction(tx)
                receipt_obj, created = self.rpt_synchro.sync_receipt(receipt)
                tx_obj, created = self.tx_synchro.sync_tx(full_tx)
                from_account, created = self.acc_synchro.sync_account(full_tx['from'])
                to_account, created = self.acc_synchro.sync_account(full_tx['to'])
                self.txrel_synchro.syn_txrel(tx_obj, from_account=from_account,
                                             to_account=to_account, block=block_obj, receipt=receipt_obj)

class BlockProcessFromTo:
    block_process = BlockProcess()

    def process(self, from_block, to_block):
        i = from_block
        while i < to_block:
            self.block_process.process(i)

class FullBlockChainLoad:
    gateway = Gateway(HTTPProviderGenerator())
    block_process = BlockProcessFromTo()

    def load(self):
        self.block_process.process(0,self.gateway.get_last_blocknumber())