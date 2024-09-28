from django.contrib import admin
from mailing.models import Client, Message, Mailing, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'last_name', 'first_name', 'patronymic')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject_of_the_letter')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'end_date', 'next_send_time')
    list_filter = ('periodicity', 'message', 'client')


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_last_attempt', 'last_attempt_time', 'response', 'attempt_status')
