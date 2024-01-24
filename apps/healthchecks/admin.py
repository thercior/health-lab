from django.contrib import admin
from healthchecks.models import TypeHealthChecks, RequestHealthChecks, SchedulingHealthChecks, MedicalAcess

admin.site.register(TypeHealthChecks)
admin.site.register(RequestHealthChecks)
admin.site.register(SchedulingHealthChecks)
admin.site.register(MedicalAcess)