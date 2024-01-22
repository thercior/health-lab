from django.urls import path
from users.views import *

app_name = 'Users'

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro_user'),
    path('login/', logar, name = 'login')
]
