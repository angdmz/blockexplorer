from django.core.management import BaseCommand

from synchro.services import BlockProcessFromTo, create_gateway


class Command(BaseCommand):
    loader = BlockProcessFromTo()
    gateway = create_gateway()

    def add_arguments(self, parser):
        parser.add_argument('--from_block', help='Bloque desde donde empezar', type=int)
        parser.add_argument('--to_block', help="Bloque hasta donde terminar", type=int)
        parser.set_defaults(from_block=0, to_block=self.gateway.get_last_blocknumber())

    def handle(self, *args, **options):
        self.loader.process(options['from_block'], options['to_block'])
