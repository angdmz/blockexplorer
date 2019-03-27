from web3 import Web3

from blkexplorer import settings


class HTTPProviderGenerator:
    url = settings.NODE_URL

    def generate_provider(self):
        return Web3(Web3.HTTPProvider(self.url))


class Gateway:
    w3: Web3

    def __init__(self, provider_generator, is_geth_poa_network=False):
        self.w3 = provider_generator.generate_provider()
        if is_geth_poa_network:
            from web3.middleware import geth_poa_middleware
            self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)

    def get_balance(self, address, measure='wei'):
        return self.w3.fromWei(self.w3.eth.getBalance(self.to_checksum_address(address)), measure)

    # precondición: la dirección es válida
    def get_contract(self, abi, address):
        return self.w3.eth.contract(abi=abi, address=address)

    # precondición: la dirección es válida
    def get_contract_functions(self, abi, address):
        contrato = self.get_contract(abi, address)
        return contrato.functions

    # precondición: la dirección es válida
    def get_contract_events(self, abi, address):
        contrato = self.get_contract(abi=abi, address=address)
        return contrato.events

    def is_valid_address(self, address):
        return self.w3.isAddress(address)

    def to_checksum_address(self, address):
        return self.w3.toChecksumAddress(address)

    def get_block(self, block_number):
        return self.w3.eth.getBlock(block_number)

    def get_tx_receipt(self, tx_hash):
        return self.w3.eth.getTransactionReceipt(tx_hash)

    def get_transaction(self, tx_hash):
        return self.w3.eth.getTransaction(tx_hash)

    def get_last_blocknumber(self):
        return self.w3.eth.blockNumber
