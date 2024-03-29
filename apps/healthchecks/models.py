from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from secrets import token_urlsafe
from datetime import timedelta


class TypeHealthChecks(models.Model):
    type_choices = (
        ('I', 'Exame de imagem'), 
        ('S', 'Exame de sangue'),
        ('U', 'Exame de urina'),
        ('D', 'Exame de DNA'),
    )
    
    name = models.CharField(max_length=50)
    type_health_checks = models.CharField(max_length=1, choices=type_choices)
    price = models.FloatField()
    available = models.BooleanField(default=True)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    
    
    def __str__(self):
        return self.name

class RequestHealthChecks(models.Model):
    choice_status = (
        ('E', 'Em análise'), 
        ('F', 'Finalizado'),
    )
    
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exam = models.ForeignKey(TypeHealthChecks, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=choice_status)
    result = models.FileField(upload_to="resultados", null=True, blank=True)
    required_password = models.BooleanField(default=False)
    password = models.CharField(max_length=6, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user} | {self.exam.name}'
    
    def badge_template(self):
        if self.status == 'E':
            class_css = 'bg-warning text-dark'
            text = 'Em análise'
        elif self.status == 'F':
            class_css = 'bg-success'
            text = 'Finalizado'
            
        return mark_safe(f'<span class="badge {class_css}">{text}</span>')

class SchedulingHealthChecks(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exams = models.ManyToManyField(RequestHealthChecks)
    scheduled = models.BooleanField(default=True)
    date = models.DateField()
    
    def __str__(self):
        return f'{self.user} | {self.date}'

class MedicalAcess(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    identifications = models.CharField(max_length=50)
    access_time = models.IntegerField() # em horas
    created_in = models.DateTimeField()
    date_start_exams = models.DateField()
    date_end_exams = models.DateField()
    token = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.token
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = token_urlsafe(6)
        super(MedicalAcess, self).save(*args, **kwargs)
    
    @property # decorador que transforma função/método simples de único retorno em propriedade
    def status(self):
        return 'Expirado' if timezone.now() > (self.created_in + timedelta(hours=self.access_time)) else 'Ativo'

    @property
    def url(self):
        return f'http://127.0.0.1:8000/exames/acesso_medico/{self.token}'
