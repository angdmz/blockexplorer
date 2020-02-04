from django.core.management import BaseCommand

from synchro.services import FullBlockChainLoad, BlockProcess, LastBlocksLoad


class Command(BaseCommand):
    block_process = LastBlocksLoad()

    def add_arguments(self, parser):
        parser.add_argument('block', help='Block number', type=int)

    def handle(self, *args, **options):
        self.block_process.load()
