from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from healthchecks.models import RequestHealthChecks
from managelab.utils import pdf_pass_exams, random_pass_generate


@staff_member_required
def manage_clients(request):
    clients = User.objects.filter(is_staff=False)
    
    fullname = request.GET.get('name')
    email = request.GET.get('email')
    
    if email:
        clients = clients.filter(email__contains=email)
    
    if fullname:
        clients = clients.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
        clients = clients.filter(full_name__contains=fullname)
        
    return render(
        request=request,
        template_name='ManageLab/manage_clients.html',
        context={
            'clients': clients,
            'fullname': fullname,
            'email': email,
        }
    )
    
@staff_member_required
def client(request, client_id):
    client = User.objects.get(id=client_id)
    exams = RequestHealthChecks.objects.filter(user=client)
    
    return render(
        request=request,
        template_name='ManageLab/client.html',
        context={
            'client': client,
            'exams': exams
        }
    )

@staff_member_required
def exam_client(request, exam_id):
    exam = RequestHealthChecks.objects.get(id=exam_id)
    
    return render(
        request=request,
        template_name='ManageLab/exam_client.html',
        context={'exam': exam}
    )

@staff_member_required
def proxy_pdf(request, exam_id):
    exam = RequestHealthChecks.objects.get(id=exam_id)
    response = exam.result.open()
    return FileResponse(response)

@staff_member_required
def generate_pass(request, exam_id):
    exam = RequestHealthChecks.objects.get(id=exam_id)
    
    if exam.password:
        # Baixar documento da senha já existente
        return FileResponse(pdf_pass_exams(exam.exam.name, exam.user, exam.password), filename='token.pdf')
    
    exam.password = random_pass_generate(6)
    exam.save()
    
    return FileResponse(pdf_pass_exams(exam.exam.name, exam.user, exam.password), filename='token.pdf')

def alter_data_exam(request, exam_id):
    exam = RequestHealthChecks.objects.get(id=exam_id)
    pdf = request.FILES.get('result')
    status = request.POST.get('status')
    required_password = request.POST.get('required_password')
    
    if required_password and (not exam.password):
        messages.add_message(request, constants.WARNING, 'Para exigir senha é necessário gerar uma primeiro')
        return redirect(reverse('ManageLab:exam_client', kwargs={'exam_id': exam_id}))
    
    exam.required_password = True if required_password else False
    
    if pdf:
        exam.result = pdf
    
    exam.status = status
    exam.save()
    messages.add_message(request, constants.SUCCESS, 'Alteração realizada com sucesso')
    
    return redirect(reverse('ManageLab:exam_client', kwargs={'exam_id': exam_id}))
