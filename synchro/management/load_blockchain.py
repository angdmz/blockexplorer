from django.core.management import BaseCommand

from synchro.services import FullBlockChainLoad


class Command(BaseCommand):

    loader = FullBlockChainLoad()

    def handle(self, *args, **options):
        self.loader.load()