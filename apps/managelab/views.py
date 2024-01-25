from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import FileResponse
from django.shortcuts import render
from healthchecks.models import RequestHealthChecks


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
