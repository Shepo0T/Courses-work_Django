from django.db import models


from users.models import User

NULLABLE = {'null': True, 'blank': True}

class Client(models.Model):
    """Модель клиента"""
    FIO = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.EmailField(max_length=150, verbose_name='почта', unique=True)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    owner = models.ForeignKey(User, **NULLABLE, verbose_name='Владелец', help_text='Введите владельца',
                              on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.FIO} {self.email}"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        ordering = ('FIO',)


class MailingSettings(models.Model):
    """Модель настроек рассылки"""
    DAILY = "Раз в день"
    WEEKLY = "Раз в неделю"
    MONTHLY = "Раз в месяц"

    PERIODICITY_CHOICES = [
        (DAILY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]

    CREATED = 'Создана'
    STARTED = 'Запущена'
    COMPLETED = 'Завершена'

    STATUS_CHOICES = [
        (COMPLETED, "Завершена"),
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
    ]

    start_time = models.DateTimeField(verbose_name='время начала рассылки')
    end_time = models.DateTimeField(verbose_name='время окончания рассылки')
    periodicity = models.CharField(max_length=50, verbose_name='периодичность', choices=PERIODICITY_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=CREATED, verbose_name='статус рассылки')

    clients = models.ManyToManyField(Client, verbose_name='клиенты рассылки')
    owner = models.ForeignKey(User, **NULLABLE, verbose_name='Владелец', help_text='Введите владельца',
                              on_delete=models.SET_NULL)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'time: {self.start_time} - {self.end_time}, periodicity: {self.periodicity}, status: {self.status},' \
               f'owner: {self.owner}'

    class Meta:
        verbose_name = 'настройки рассылки'
        verbose_name_plural = 'настройки рассылки'

        permissions = [
            (
                'change_status',
                'Can change status'
            )
        ]


class Message(models.Model):
    """Модель сообщений"""
    title = models.CharField(max_length=100, verbose_name='тема письма')
    text = models.TextField(verbose_name='тело письма')
    mailing_list = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='рассылка',
                                     related_name='messages', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Log(models.Model):
    """Модель логов"""
    time = models.DateTimeField(verbose_name='дата и время последней попытки', auto_now_add=True)
    status = models.BooleanField(verbose_name='статус попытки')
    server_response = models.CharField(verbose_name='ответ почтового сервера', **NULLABLE)

    mailing_list = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент рассылки')

    def __str__(self):
        return f'{self.time} {self.status}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'

class TryMailing(models.Model):
    SUCCESS = "success"
    FAILURE = "failure"
    STATUSES = [(SUCCESS, "success"), (FAILURE, "failure")]
    last_try = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата последней попытки"
    )
    status = models.CharField(choices=STATUSES, default=SUCCESS, verbose_name="Статус")
    response = models.TextField(**NULLABLE, verbose_name="Ответ")
    mailing = models.ForeignKey(
        MailingSettings,
        on_delete=models.CASCADE,
        related_name="logs",
        verbose_name="Рассылка",
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ("status",)

    def __str__(self):
        return f"{self.status}"