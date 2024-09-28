import logging

import pytz
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Q
from mailing.models import Attempt, Mailing
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(level=logging.DEBUG)


def start():
    logging.debug('Планировщик запущен')
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)
    scheduler.start()
    logging.debug('Задача send_mailing запланирована')


def send_email(subject_of_the_letter, body_of_the_letter, email_from, email):
    send_mail(subject_of_the_letter, body_of_the_letter, email_from, email)


def send_mailing():
    logging.debug('Задача send_mailing запущена')
    try:
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)
        
        mailings = Mailing.objects.filter(
            Q(start_date__lte=current_datetime) &
            Q(end_date__gte=current_datetime) &
            Q(status='launched')
        )
        
        for mailing in mailings:
            last_attempt = Attempt.objects.filter(mailing=mailing).order_by('-date_last_attempt').first()
            if last_attempt:
                time_diff = current_datetime - last_attempt.date_last_attempt
                if mailing.periodicity == 'daily' and time_diff.days >= 1:
                    next_send_time = last_attempt.date_last_attempt + timedelta(days=1, hours=mailing.start_date.hour,
                                                                                minutes=mailing.start_date.minute)
                    if current_datetime >= next_send_time:
                        send_email(mailing.message.subject_of_the_letter, mailing.message.body_of_the_letter,
                                   settings.EMAIL_HOST_USER, [client.email for client in mailing.client.all()])
                elif mailing.periodicity == 'weekly' and time_diff.days >= 7:
                    next_send_time = last_attempt.date_last_attempt + timedelta(days=7, hours=mailing.start_date.hour,
                                                                                minutes=mailing.start_date.minute)
                    if current_datetime >= next_send_time:
                        send_email(mailing.message.subject_of_the_letter, mailing.message.body_of_the_letter,
                                   settings.EMAIL_HOST_USER, [client.email for client in mailing.client.all()])
                elif mailing.periodicity == 'monthly' and time_diff.days >= 30:
                    next_send_time = last_attempt.date_last_attempt + timedelta(days=30, hours=mailing.start_date.hour,
                                                                                minutes=mailing.start_date.minute)
                    if current_datetime >= next_send_time:
                        send_email(mailing.message.subject_of_the_letter, mailing.message.body_of_the_letter,
                                   settings.EMAIL_HOST_USER, [client.email for client in mailing.client.all()])
            else:
                send_email(mailing.message.subject_of_the_letter, mailing.message.body_of_the_letter,
                           settings.EMAIL_HOST_USER, [client.email for client in mailing.client.all()])
    except Exception as e:
        logging.error('Ошибка при создании рассылки: %s', e)
    logging.debug('Задача send_mailing завершена')
