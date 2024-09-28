from django.apps import AppConfig


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    def ready(self):
        from .management.commands import apsch
        apsch.Command().handle()
        print('Служба почты запущена!')
