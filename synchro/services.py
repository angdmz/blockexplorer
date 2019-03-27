import datetime

from django.db import transaction

from blkexplorer import settings
from dapp.gateway import Gateway, HTTPProviderGenerator
from ethereum.models import Transaction, Block, Account, TransactionRelationship

import logging

logger = logging.getLogger('cmd-logger')


class TransactionSynchro:
    gateway = Gateway(HTTPProviderGenerator())
    tx_manager = Transaction.objects

    def sync_tx(self, tx):
        logger.info("Syncing tx: {}".format(tx['hash'].hex()))
        tx_model, created = self.tx_manager.update_or_create(
            hash=tx['hash'].hex(),
            defaults=
            {
                'gas': tx['gas'],
                'gas_price': tx['gasPrice'],
                'input': tx['input'],
                'value': tx['value'],
                'transaction_index': tx['transactionIndex'],
                'nonce': tx['nonce']}
        )
        return tx_model, created


class BlockSynchro:
    blk_manager = Block.objects

    def sync_block(self, block):
        logger.debug("Syncing block: {}".format(str(block)))
        logger.info("Syncing block number: {}".format(str(block['number'])))
        blk_model, created = self.blk_manager.update_or_create(
            hash=block['hash'].hex(),
            defaults=
            {
                'gas_used': block['gasUsed'],
                'gas_limit': block['gasLimit'],
                'number': block['number'],
                'timestamp': datetime.datetime.fromtimestamp(block['timestamp']),
                'size': block['size'],
                'state_root': block['stateRoot'],
                'transactions_root': block['transactionsRoot'],
                'total_difficulty': block['totalDifficulty'],
                'difficulty': block['difficulty'],
                'nonce': block['nonce'],
                'parent_hash': block['parentHash'],
            }
        )
        return blk_model, created


class ReceiptSynchro:
    rpt_manager = Block.objects

    def sync_receipt(self, rpt):
        logger.info("Syncing rpt: {}".format(rpt['hash'].hex()))
        rpt_manager, created = self.rpt_manager.update_or_create(
            hash=rpt['hash'].hex(),
            defaults=
            {
                'cumulative_gas_used': rpt['gasUsed'],
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
    gateway = Gateway(HTTPProviderGenerator(), settings.IS_POA_CHAIN)
    blk_synchro = BlockSynchro()
    rpt_synchro = ReceiptSynchro()
    tx_synchro = TransactionSynchro()
    acc_synchro = AccountSynchro()
    txrel_synchro = TransactionRelationSynchro()

    def process(self, block_number):
        block = self.gateway.get_block(block_number)
        logger.info("Processing block: {}".format(str(block_number)))
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
        logger.info("Process from block {} to block {}".format(str(from_block), str(to_block)))
        while i < to_block:
            self.block_process.process(i)
            i = i + 1


class FullBlockChainLoad:
    gateway = Gateway(HTTPProviderGenerator())
    block_process = BlockProcessFromTo()

    def load(self):
        logger.info("Starting blockchain full load")
        self.block_process.process(0, self.gateway.get_last_blocknumber())
