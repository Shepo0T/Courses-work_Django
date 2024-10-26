from django.forms import ModelForm
from mailings.models import MailingSettings, Message, Log, Client

class StyleFormMixin:
    """Миксин"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingSettingsForm(StyleFormMixin, ModelForm):
    """Форма настроек рассылки"""
    class Meta:
        model = MailingSettings
        fields = ('start_time', 'end_time', 'periodicity', 'status', 'clients',)


class PermMailingSettingsForm(StyleFormMixin, ModelForm):
    """Форма настроек рассылки для тех у кого частичные разрешения"""
    class Meta:
        model = MailingSettings
        fields = ('status', )


class MessageForm(StyleFormMixin, ModelForm):
    """Форма сообщений"""
    class Meta:
        model = Message
        fields = ('title', 'text',)


class ClientForm(StyleFormMixin, ModelForm):
    """Форма клиента"""
    class Meta:
        model = Client
        fields = ('FIO', 'email', 'comment',)