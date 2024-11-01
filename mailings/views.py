from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.forms import inlineformset_factory
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from mailings.models import Client, MailingSettings, Message, Log
from mailings.forms import MessageForm, MailingSettingsForm, ClientForm, PermMailingSettingsForm
from blog.models import Blog

class ClientListView(LoginRequiredMixin, ListView):
    """Список клиентов"""
    model = Client

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Client.objects.all()
        else:
            return Client.objects.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Создание клиента"""
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailings:clients_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Обновление клиента"""
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailings:clients_list')

    def test_func(self):
        client = self.get_object()
        return self.request.user.is_superuser or self.request.user == client.owner


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Просмотр одного клиента"""
    model = Client

    def test_func(self):
        client = self.get_object()
        return self.request.user.is_superuser or self.request.user == client.owner


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление клиента"""
    model = Client
    success_url = reverse_lazy('mailings:clients_list')

    def test_func(self):
        client = self.get_object()
        return self.request.user.is_superuser or self.request.user == client.owner


class MailingSettingsDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Просмотр одной рассылки"""
    model = MailingSettings

    def test_func(self):
        mailing_settings = self.get_object()
        return (self.request.user.is_superuser or self.request.user == mailing_settings.owner or
                self.request.user.has_perm(
                    'mailings.view_mailingsettings'))


class MailingSettingsListView(LoginRequiredMixin, ListView):
    """Просмотр списка рассылок"""
    model = MailingSettings

    def cache_example(self):
        if settings.CACHE_ENABLE:
            key = f'mailset_list'
            mailset_list = cache.get(key)
            print(mailset_list)
            if mailset_list is None:
                mailset_list = MailingSettings.objects.all()
                cache.set(key, mailset_list)
        else:
            mailset_list = MailingSettings.objects.all()
        return mailset_list

    def get_queryset(self):
        return self.cache_example()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        user = self.request.user
        if user.is_superuser:
            context_data['all'] = MailingSettings.objects.count()
            context_data['active'] = MailingSettings.objects.filter(status=MailingSettings.STARTED).count()
            mailing_list = context_data['object_list']
            clients = [[client.email for client in mailing.clients.all()] for mailing in mailing_list]
            context_data['clients_count'] = len(clients)
        else:
            mailing_list = MailingSettings.objects.filter(owner=user)
            clients = [[client.email for client in mailing.clients.all()] for mailing in mailing_list]
            context_data['all'] = mailing_list.count()
            context_data['active'] = mailing_list.filter(status=MailingSettings.STARTED).count()
            context_data['clients_count'] = len(clients)
        random_blogs = Blog.objects.order_by('?')[:3]
        article_titles = [blog.title for blog in random_blogs]
        article_pk = [blog.pk for blog in random_blogs]
        context_data['articles'] = dict(zip(article_titles, article_pk))
        return context_data


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    """Создание рассылки"""
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailings:distribution_list')

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(MailingSettings, Message, extra=1, form=MessageForm)

        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST)
        else:
            context_data['formset'] = MessageFormset()

        return context_data

    def get_success_url(self):
        return reverse('mailings:distribution_list')


class MailingSettingsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление рассылки"""
    model = MailingSettings
    permission_required = 'mailings.delete_mailingsettings'

    def test_func(self):
        mailing_settings = self.get_object()
        return self.request.user.is_superuser or self.request.user == mailing_settings.owner

    def get_success_url(self):
        return reverse('mailings:distribution_list')


class MailingSettingsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Обновление рассылки"""
    model = MailingSettings
    form_class = MailingSettingsForm

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('mailings.change_status')

    def get_form_class(self):
        if self.request.user.has_perm('mailings.change_status') and not self.request.user.is_superuser:
            return PermMailingSettingsForm
        return MailingSettingsForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(MailingSettings, Message, extra=1, form=MessageForm)

        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MessageFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailings:distribution_detail', args=[self.object.pk])


class LogListView(LoginRequiredMixin, ListView):
    """Просмотр списка логов"""
    model = Log

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        user = self.request.user
        mailing_list = MailingSettings.objects.filter(owner=user).first()
        if user.is_superuser:
            context_data['all'] = Log.objects.count()
            context_data['success'] = Log.objects.filter(
                status=True).count()
            context_data['error'] = Log.objects.filter(status=False).count()
        else:
            user_logs = Log.objects.filter(mailing_list=mailing_list)
            context_data['all'] = user_logs.count()
            context_data['success'] = user_logs.filter(
                status=True).count()
            context_data['error'] = user_logs.filter(status=False).count()
        return context_data

def toggle_activity_mailings(request, pk):
    mailings = get_object_or_404(MailingSettings, pk=pk)
    if mailings.is_active:
        mailings.is_active = False
    else:
        mailings.is_active = True

    mailings.save()

    return redirect(reverse('mailings:distribution_list'))