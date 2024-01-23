from django.urls import path
from healthchecks.views import *

app_name = 'HealthChecks'

urlpatterns = [
    path('solicitar_exames/', request_exams, name='request_exam'),
    path('checkout_pedido/', close_order, name='close_order'),
    path('gerenciar_pedidos/', manage_order, name='manage_order'),
    path('cancelar_pedido/<int:order_id>', order_cancel, name='order_cancel'),
    path('gerenciar_exames/', manage_exams, name='manage_exam'),
    path('abri_exame/<int:exam_id>', open_exam, name='open_exam'),
]
