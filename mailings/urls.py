from django.urls import path

from mailings.views import MailingSettingsDetailView, MailingSettingsListView, MailingSettingsCreateView, \
    MailingSettingsDeleteView, MailingSettingsUpdateView, ClientListView, ClientCreateView, ClientUpdateView, \
    LogListView, ClientDetailView, ClientDeleteView, toggle_activity_mailings

urlpatterns = [
    path('log/', LogListView.as_view(), name='log_list'),
    path('clients/edit/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),
    path('clients/create/', ClientCreateView.as_view(), name='create_client'),
    path('clients/', ClientListView.as_view(), name='clients_list'),
    path('distribution/<int:pk>/', MailingSettingsDetailView.as_view(), name='distribution_detail'),
    path('delete/<int:pk>/', MailingSettingsDeleteView.as_view(), name='distribution_delete'),
    path('', MailingSettingsListView.as_view(), name='distribution_list'),
    path('create/', MailingSettingsCreateView.as_view(), name='create_distribution'),
    path('edit/<int:pk>/', MailingSettingsUpdateView.as_view(template_name='mailings/mailingsettings_update_form.html'),
         name='distribution_edit'),
    path('clients/<int:pk>', ClientDetailView.as_view(), name='detail_client'),
    path('clients/delete/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
    path('activity_mailings/<int:pk>/', toggle_activity_mailings, name='toggle_activity_mailings'),
]