from django.contrib import admin

from mailings.models import MailingSettings, Message, Log, Client


@admin.register(MailingSettings)
class MailingListSettingsAdmin(admin.ModelAdmin):
    """Админка рассылки"""
    list_display = ('pk', 'start_time', 'end_time', 'periodicity', 'status',)
    list_filter = ('start_time', 'end_time', 'periodicity', 'status',)
    search_fields = ('start_time', 'end_time',)

@admin.register(Message)
class MessageListSettingsAdmin(admin.ModelAdmin):
    """Админка сообщения"""
    list_display = ('pk', 'title', 'mailing_list',)
    list_filter = ['mailing_list', ]
    search_fields = ['title', 'text', ]


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    """Админка логов"""
    list_display = ['pk', 'mailing_list', 'time', 'status', 'server_response', ]
    list_filter = ['mailing_list', 'status', ]
    search_fields = ['mailing_list', 'time', 'status', ]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Админка клиента"""
    list_display = ('pk', 'email', 'FIO')
    list_filter = ('FIO',)
    search_fields = ('email', 'FIO', 'comment',)