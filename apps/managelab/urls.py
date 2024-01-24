from django.urls import path
from managelab.views import *

app_name = 'ManageLab'

urlpatterns = [
    path('gerenciar_clientes/', manage_clients, name='manage_clients'),
    path('clients/<int:client_id>', client, name='client'),
]
