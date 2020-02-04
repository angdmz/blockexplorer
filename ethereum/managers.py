from django.db import models


class TxNonExistent(Exception):
    pass

class TransactionManager(models.Manager):
    def find_by_hash(self, hash_str):
        try:
            res = self.get(hash=hash_str)
        except Exception as e:
            raise TxNonExistent(e)
        return res


class BlockNonExistent(Exception):
    pass


class BlockManager(models.Manager):
    def find_by_hash(self, hash_str):
        try:
            res = self.get(hash=hash_str)
        except Exception as e:
            raise BlockNonExistent(e)
        return res

    def find_by_number(self, number):
        try:
            res = self.get(number=number)
        except Exception as e:
            raise BlockNonExistent(e)
        return res

    def last_block(self):
        return self.latest('number')