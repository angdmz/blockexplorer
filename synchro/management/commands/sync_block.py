from django.core.management import BaseCommand

from synchro.services import FullBlockChainLoad, BlockProcess


class Command(BaseCommand):
    block_process = BlockProcess()

    def add_arguments(self, parser):
        parser.add_argument('block', help='Block number', type=int)

    def handle(self, *args, **options):
        self.block_process.process(options['block'])
