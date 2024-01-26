from django.contrib import admin
from healthchecks.models import TypeHealthChecks, RequestHealthChecks, SchedulingHealthChecks, MedicalAcess

@admin.register(TypeHealthChecks)
class TypeHealthChecksAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_health_checks', 'price', 'available')

@admin.register(RequestHealthChecks)
class RequestHealthChecksAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'status', 'required_password', 'result')

# @admin.register(SchedulingHealthChecks)
# class SchedulingHealthChecksAdmin(admin.ModelAdmin):
#     list_display = ('scheduled', 'date')

@admin.register(MedicalAcess)
class MedicalAcessAdmin(admin.ModelAdmin):
    list_display = ('user', 'identifications', 'access_time', 'token')

# admin.site.register(TypeHealthChecks)
# admin.site.register(RequestHealthChecks)
admin.site.register(SchedulingHealthChecks)
# admin.site.register(MedicalAcess)