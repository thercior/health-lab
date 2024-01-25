from django.urls import path
from managelab.views import *

app_name = 'ManageLab'

urlpatterns = [
    path('gerenciar_clientes/', manage_clients, name='manage_clients'),
    path('clientes/<int:client_id>', client, name='client'),
    path('exame_cliente/<int:exam_id>', exam_client, name='exam_client'),
    path('proxy_pdf/<int:exam_id>', proxy_pdf, name='proxy_pdf'),
    path('gerar_senha/<int:exam_id>', generate_pass, name='generate_pass')
]
