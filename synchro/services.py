from django.db import transaction
from django.conf import settings
from gateway.gateway import generate_http_gateway
from ethereum.models import Transaction, Block, Account, TransactionRelationship, Receipt, SmartContract

import logging

from gateway.utils import HexBytesToDict

logger = logging.getLogger('cmd-logger')


def create_gateway():
    return generate_http_gateway(settings.NODE_URL, settings.IS_POA)


class TransactionSynchro:
    gateway = create_gateway()
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
                'nonce': tx['nonce']
            }
        )
        return tx_model, created


class ReceiptSynchro:
    rpt_manager = Receipt.objects

    def sync_receipt(self, rpt):
        logger.info("Syncing rpt: {}".format(rpt['transactionHash'].hex()))
        rpt_manager, created = self.rpt_manager.update_or_create(
            transaction_hash=rpt['transactionHash'].hex(),
            defaults=
            {
                'cumulative_gas_used': rpt['cumulativeGasUsed'],
                'gas_used': rpt['gasUsed'],
                'status': rpt['status'],
            }
        )
        return rpt_manager, created


class AccountSynchro:
    acc_manager = Account.objects

    def sync_account(self, address):
        if address is not None:
            acc_model, created = self.acc_manager.update_or_create(public_key=address)
            return acc_model, created
        return None, False


class SmartContractSynchro:
    smart_contract_manager = SmartContract.objects

    def sync_smart_contract(self, receipt, tx_rel):
        if receipt['contractAddress'] is not None:
            sc_model, created = self.smart_contract_manager.update_or_create(public_key=receipt['contractAddress'],
                                                                             defaults={
                                                                                 'deployer': tx_rel.from_account,
                                                                                 'deploy_tx': tx_rel
                                                                             }
                                                                             )
            return sc_model, created
        return None, False


class BlockSynchro:
    blk_manager = Block.objects
    acc_sync = AccountSynchro()

    def sync_block(self, block):
        logger.debug("Syncing block: {}".format(str(block)))
        logger.info("Syncing block number: {}".format(str(block['number'])))
        acc, created = self.acc_sync.sync_account(block['miner'])
        blk_model, created = self.blk_manager.update_or_create(
            hash=block['hash'].hex(),
            defaults=
            {
                'gas_used': block['gasUsed'],
                'gas_limit': block['gasLimit'],
                'number': block['number'],
                'timestamp': block['timestamp'],
                'size': block['size'],
                'state_root': block['stateRoot'].hex(),
                'transactions_root': block['transactionsRoot'].hex(),
                'receipts_root': block['receiptsRoot'].hex(),
                'total_difficulty': block['totalDifficulty'],
                'difficulty': block['difficulty'],
                'nonce': int(block['nonce'].hex(), 16),
                'parent_hash': block['parentHash'].hex(),
                'sha3_uncles': block['sha3Uncles'].hex(),
                'mix_hash': block['mixHash'].hex(),
                'miner': acc
            }
        )
        return blk_model, created


class TransactionRelationSynchro:
    txrel_manager = TransactionRelationship.objects

    def syn_txrel(self, tx, **options):
        return self.txrel_manager.update_or_create(transaction=tx, defaults=options)


class BlockProcess:
    gateway = create_gateway()
    blk_synchro = BlockSynchro()
    rpt_synchro = ReceiptSynchro()
    tx_synchro = TransactionSynchro()
    acc_synchro = AccountSynchro()
    txrel_synchro = TransactionRelationSynchro()
    smart_contract_synchro = SmartContractSynchro()
    hex_to_dict = HexBytesToDict()

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
                txrel, created = self.txrel_synchro.syn_txrel(tx_obj, from_account=from_account,
                                                              to_account=to_account, block=block_obj,
                                                              receipt=receipt_obj)
                self.smart_contract_synchro.sync_smart_contract(receipt, txrel)


class BlockProcessFromTo:
    block_process = BlockProcess()

    def process(self, from_block, to_block):
        i = from_block
        logger.info("Process from block {} to block {}".format(str(from_block), str(to_block)))
        while i < to_block:
            self.block_process.process(i)
            i = i + 1


class FullBlockChainLoad:
    gateway = create_gateway()
    block_process = BlockProcessFromTo()

    def load(self):
        logger.info("Starting blockchain full load")
        self.block_process.process(0, self.gateway.get_last_blocknumber())


class LastBlocksLoad:
    gateway = create_gateway()
    block_process = BlockProcessFromTo()
    block_manager = Block.objects

    def load(self):
        last_loaded_block = self.block_manager.last_block_number()
        logger.info("Loading from block {}".format(str(last_loaded_block)))
        self.block_process.process(last_loaded_block, self.gateway.get_last_blocknumber())
