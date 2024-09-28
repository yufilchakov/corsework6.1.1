from django.db import models

from users.models import User


class Client(models.Model):
    """Модель клиента"""
    
    email = models.EmailField(unique=True, verbose_name='Контактный email')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    patronymic = models.CharField(max_length=20, verbose_name='Отчество')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Пользователь", blank=True, null=True)
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        permissions = [
            ('man_view_the_list_of_service_users', 'can view the list of service users'),
            ('may_block_users_of_the_service', 'may block users of the service')
        ]
    
    def __str__(self):
        return self.email


class Message(models.Model):
    """Модель сообщения"""
    
    subject_of_the_letter = models.CharField(max_length=255, verbose_name='Тема письма')
    body_of_the_letter = models.TextField(verbose_name='Сообщение')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Пользователь", blank=True, null=True)
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        permissions = [
            ('can_view_messages', 'Can view messages'),
            ('can_edit_messages', 'Can edit messages')
        ]
    
    def __str__(self):
        return self.subject_of_the_letter


class Mailing(models.Model):
    """Модель рассылки"""
    
    STATUS_CHOICES = [
        ('create', 'Создана'),
        ('launched', 'Запущена'),
        ('completed', 'Завершена'),
    ]
    
    PERIODICITY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]
    
    start_date = models.DateTimeField(verbose_name='Дата и время начала рассылки')
    end_date = models.DateTimeField(verbose_name='Дата и время окончания рассылки')
    next_send_time = models.DateTimeField(verbose_name='Дата и время следующей отправки рассылки', null=True,
                                          blank=True)
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES,
                                   verbose_name='Периодичность рассылки письма')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='create', verbose_name='Статус рассылки')
    message = models.OneToOneField(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    client = models.ManyToManyField(Client, verbose_name='Клиенты рассылки')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Пользователь", blank=True, null=True)
    
    class Meta:
        
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('can_view_any_mailings', 'Can view any mailings'),
            ('can_disable_mailings', 'Can disable mailings')
        ]

    def __str__(self):
        return f'Рассылка, начинающаяся в {self.start_date}'


class Attempt(models.Model):
    """Модель попытки рассылки"""
    
    ATTEMPT_STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failure', 'Не успешно'),
    ]
    
    date_last_attempt = models.DateTimeField(null=True, blank=True, verbose_name='Дата последней попытки')
    last_attempt_time = models.DateTimeField(null=True, blank=True, verbose_name='Время последней попытки')
    response = models.ForeignKey(Mailing, related_name='responses', on_delete=models.CASCADE,
                                 verbose_name='Ответ почтового сервера, если он был')
    attempt_status = models.TextField(max_length=10, choices=ATTEMPT_STATUS_CHOICES, verbose_name='Статус попытки')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')
    
    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
    
    def __str__(self):
        return f'Попытка рассылки в {self.date_last_attempt} - {self.last_attempt_time}, {self.attempt_status}'
