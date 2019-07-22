from datetime import datetime

from django.test import TestCase

# Create your tests here.
from hexbytes import HexBytes

from ethereum.models import Transaction, Block
from ethereum.managers import TxNonExistent, BlockNonExistent
from synchro.services import TransactionSynchro, BlockSynchro


class TestCases:
    tx = {
        'blockHash': '0x4e3a3754410177e6937ef1f84bba68ea139e8d1a2258c5f85db9f1cd715a1bdd',
        'blockNumber': 46147,
        'from': '0xa1e4380a3b1f749673e270229993ee55f35663b4',
        'gas': 21000,
        'gasPrice': 50000000000000,
        'hash': HexBytes('0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060'),
        'input': '0x',
        'nonce': 0,
        'to': '0x5df9b87991262f6ba471f09758cde1c0fc1de734',
        'transactionIndex': 0,
        'value': 31337,
    }
    another_tx = {
        'blockHash': '0x4e3a3754410177e6937ef1f84bba68ea139e8d1a2258c5f85db9f1cd715a1bdd',
        'blockNumber': 46147,
        'from': '0xa1e4380a3b1f749673e270229993ee55f35663b4',
        'gas': 21000,
        'gasPrice': 50000000000000,
        'hash': HexBytes('0x23l4j5hl23k4h58bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22061'),
        'input': '0x',
        'nonce': 0,
        'to': '0x5df9b87991262f6ba471f09758cde1c0fc1de734',
        'transactionIndex': 0,
        'value': 31337,
    }
    block = {
        'difficulty': 49824742724615,
        'extraData': '0xe4b883e5bda9e7a59ee4bb99e9b1bc',
        'gasLimit': 4712388,
        'gasUsed': 21000,
        'hash': HexBytes('0xc0f4906fea23cf6f3cce98cb44e8e1449e455b28d684dfa9ff65426495584de6'),
        'logsBloom': '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        'miner': '0x61c808d82a3ac53231750dadc13c777b59310bd9',
        'nonce': int('0x3b05c6d5524209f1', 16),
        'number': 2000000,
        'parentHash': '0x57ebf07eb9ed1137d41447020a25e51d30a0c272b5896571499c82c33ecb7288',
        'receiptRoot': '0x84aea4a7aad5c5899bd5cfc7f309cc379009d30179316a2a7baa4a2ea4a438ac',
        'sha3Uncles': '0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347',
        'size': 650,
        'stateRoot': '0x96dbad955b166f5119793815c36f11ffa909859bbfeb64b735cca37cbf10bef1',
        'timestamp': 1470173578,
        'totalDifficulty': 44010101827705409388,
        'transactions': ['0xc55e2b90168af6972193c1f86fa4d7d7b31a29c156665d15b9cd48618b5177ef'],
        'transactionsRoot': '0xb31f174d27b99cdae8e746bd138a01ce60d8dd7b224f7c60845914def05ecc58',
        'uncles': [],
    }

    another_block = {
        'difficulty': 49824742724615,
        'extraData': '0xe4b883e5bda9e7a59ee4bb99e9b1bc',
        'gasLimit': 4712388,
        'gasUsed': 21000,
        'hash': '0x3457899bbhb3cf6f3cce98cb44e8e1449e455b28d684dfa9ff65426495584de6',
        'logsBloom': '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        'miner': '0x61c808d82a3ac53231750dadc13c777b59310bd9',
        'nonce': int('0x3b05c6d5524209f1', 16),
        'number': 2000000,
        'parentHash': '0x57ebf07eb9ed1137d41447020a25e51d30a0c272b5896571499c82c33ecb7288',
        'receiptRoot': '0x84aea4a7aad5c5899bd5cfc7f309cc379009d30179316a2a7baa4a2ea4a438ac',
        'sha3Uncles': '0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347',
        'size': 650,
        'stateRoot': '0x96dbad955b166f5119793815c36f11ffa909859bbfeb64b735cca37cbf10bef1',
        'timestamp': 1470173578,
        'totalDifficulty': 44010101827705409388,
        'transactions': ['0xc55e2b90168af6972193c1f86fa4d7d7b31a29c156665d15b9cd48618b5177ef'],
        'transactionsRoot': '0xb31f174d27b99cdae8e746bd138a01ce60d8dd7b224f7c60845914def05ecc58',
        'uncles': [],
    }

class TestSynchroTransaction(TestCase, TestCases):

    def setUp(self):
        self.synchro = TransactionSynchro()
        self.tx_manager = Transaction.objects

    def test_creation(self):
        tx = self.tx
        self.assertRaises(TxNonExistent, self.tx_manager.find_by_hash, hash_str=tx['hash'])
        tx_obj, created = self.synchro.sync_tx(tx)
        self.assertTrue(tx_obj is not None)
        self.assertTrue(created)
        self.assertEquals(tx['hash'], tx_obj.hash)
        self.assertEquals(tx['gasPrice'], tx_obj.gas_price)

    def test_update(self):
        tx = self.another_tx
        tx_obj, created = self.synchro.sync_tx(tx)
        self.assertTrue(tx_obj is not None)
        self.assertTrue(created)
        tx['value'] = 237492374289
        new_tx_obj, new_created = self.synchro.sync_tx(tx)
        self.assertTrue(new_tx_obj is not None)
        self.assertFalse(new_created)
        self.assertEquals(tx['value'], new_tx_obj.value)
        self.assertEquals(tx['hash'], new_tx_obj.hash)
        self.assertEquals(tx['hash'], tx_obj.hash)


class TestBlockSynchro(TestCase, TestCases):

    def setUp(self):
        self.synchro = BlockSynchro()
        self.block_manager = Block.objects

    def test_create(self):
        block = self.block
        self.assertRaises(BlockNonExistent, self.block_manager.find_by_hash, hash_str=block['hash'])
        block_obj, created = self.synchro.sync_block(block)
        self.assertTrue(created)
        self.assertFalse(block_obj is None)
        self.assertEquals(block['hash'], block_obj.hash)
        self.assertEquals(block['timestamp'], datetime.timestamp(block_obj.timestamp))

    def test_update(self):
        block = self.another_block
        block_obj, created = self.synchro.sync_block(block)
        self.assertTrue(created)
        block['size'] = 100000
        new_block_obj, new_created = self.synchro.sync_block(block)
        self.assertFalse(new_created)
        self.assertEquals(block['size'], new_block_obj.size)
        self.assertEquals(block['hash'], block_obj.hash)
        self.assertEquals(block['hash'], new_block_obj.hash)
