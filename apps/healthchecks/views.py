from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from healthchecks.models import TypeHealthChecks, SchedulingHealthChecks, RequestHealthChecks
from datetime import datetime
import locale


@login_required
def request_exams(request):
    type_exams = TypeHealthChecks.objects.all()
    
    if request.method == 'GET':
        return render(request, 'HealthChecks/request_exams.html', {'type_exams': type_exams})
    
    if request.method == 'POST':
        # Caputa os dados de exames selecionados
        exams_id = request.POST.getlist('exams')
        request_exams = TypeHealthChecks.objects.filter(id__in=exams_id)
        price_total = 0
        price_total = sum(i.price for i in request_exams if i.available) 
        
        # capturar data atual para exibir no template
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8') # Define a região para exibir em pt-BR
        
        date_now = datetime.now()
        day_week = date_now.strftime('%A')
        day_moth = date_now.day
        moth = date_now.strftime('%B')
        year = date_now.year
        
        date_display = f'{day_week}, {day_moth} de {moth} de {year}'
        
        return render(
            request=request, 
            template_name='HealthChecks/request_exams.html',
            context={
                'request_exams': request_exams,
                'price_total': price_total,
                'type_exams': type_exams,
                'date_display': date_display
            }
        )

@login_required
def close_order(request):
    exams_id = request.POST.getlist('exams')
    request_exams = TypeHealthChecks.objects.filter(id__in=exams_id)
    
    order_exam = SchedulingHealthChecks(user=request.user, date=datetime.now())
    order_exam.save()
    
    for exam in request_exams:
        request_exams_temp = RequestHealthChecks(
            user=request.user,
            exam=exam,
            status='E',
        )
        
        request_exams_temp.save()
        order_exam.exams.add(request_exams_temp)
    
    order_exam.save()
    success_message = 'Pedido de exame concluído com sucesso!'
    messages.add_message(request, constants.SUCCESS, success_message)
    
    return redirect('HealthChecks:manage_order')

@login_required
def manage_order(request):
    order_exams = SchedulingHealthChecks.objects.filter(user=request.user)
    return render(
        request=request, 
        template_name='HealthChecks/manage_order.html', 
        context={'order_exams': order_exams}
    )

@login_required
def order_cancel(request, order_id):
    order = SchedulingHealthChecks.objects.get(id=order_id)
    
    if order.user != request.user:
        message_denied = 'Permissão negada! Este pedido não é seu'
        messages.add_message(request, constants.ERROR, message_denied)
        return redirect('HealthChecks:manage_order')
    
    order.scheduled = False
    order.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido cancelado com sucesso!')
    return redirect('HealthChecks:manage_order')

@login_required
def manage_exams(request):
    exams = RequestHealthChecks.objects.filter(user=request.user)
    
    return render(
        request=request,
        template_name='HealthChecks/manage_exams.html',
        context={'exams': exams},
    )

@login_required
def open_exam(request, exam_id):
    try:
        exam = RequestHealthChecks.objects.get(id=exam_id)
    except RequestHealthChecks.DoesNotExist:
        raise Http404('Exame não encontrado')
    
    #validar se o exame é do usuário
    if exam.user != request.user:
        messages.add_message(request, constants.WARNING, 'Atenção! Este exame não percente ao usuário atual')
        return redirect('HealthChecks:manage_exam')
    
    # Verifica se o pdf existe
    if exam.result:
            
        if not exam.required_password:
            return redirect(exam.result.url)
        else: 
            return redirect(reverse('HealthChecks:required_pass_exam', kwargs={'exam_id': exam_id}))
        
    message_alert = 'Não foi encontrado o resultado do exame. Por favor, entrar em contato com a HealthLAB.'
    messages.add_message(request, constants.WARNING, message_alert)
    return redirect('HealthChecks:manage_exam')

@login_required
def required_password_exam(request, exam_id):
    exam = RequestHealthChecks.objects.get(id=exam_id)
    
    if request.method == 'GET':
        return render(
            request=request,
            template_name='HealthChecks/required_pass_exams.html',
            context={"exam": exam}
        )
    
    if request.method == 'POST':
        password = request.POST.get('password')
        
        if exam.user != request.user:
            messages.add_message(request, constants.WARNING, 'Atenção! Este exame não percente ao usuário atual')
        
        if password == exam.password and exam.result:
            return redirect(exam.result.url)
        else:
            messages.add_message(request, constants.ERROR, 'Senha Inválida!')
            return redirect(reverse('HealthChecks:required_pass_exam', kwargs={'exam_id': exam_id}))
        