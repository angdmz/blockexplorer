from django.core.management import BaseCommand

from synchro.services import LastBlocksLoad


class Command(BaseCommand):
    block_process = LastBlocksLoad()

    def handle(self, *args, **options):
        self.block_process.load()
