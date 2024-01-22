from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from django.http import HttpResponse


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'Users/cadastro.html')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.add_message(request, constants.ERROR, 'As senhas não são iguais!!')
            return redirect('Users:cadastro_user')
        
        if len(password) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve ser maior que 6 caracteres')
            return redirect('Users:cadastro_user')
        
        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
        except Exception as e:
            error_message = f'Erro ao cadastrar o usuário: {e}'
            messages.add_message(request, constants.ERROR, error_message)
            return redirect('Users:cadastro_user')
    
    return redirect('Users:cadastro_user')
