import logging
from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler

from mailing.services import send_mailing

logging.basicConfig(level=logging.DEBUG)


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        logging.debug('Команда apsch запущена')
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_mailing, 'interval', seconds=10)
        scheduler.start()
        logging.info('launched')
        try:
            while True:
                pass
        except KeyboardInterrupt:
            scheduler.shutdown()
            logging.info('completed')
            