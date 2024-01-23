from django.urls import path
from healthchecks.views import *

app_name = 'HealthChecks'

urlpatterns = [
    path('solicitar_exames/', request_exams, name='request_exam'),
    path('checkout_pedido/', close_order, name='close_order')
]
