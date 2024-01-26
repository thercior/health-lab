from django.contrib import admin
from healthchecks.models import TypeHealthChecks, RequestHealthChecks, SchedulingHealthChecks, MedicalAcess
from import_export.admin import ImportExportMixin

@admin.register(TypeHealthChecks)
class TypeHealthChecksAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('available', 'name', 'type_health_checks', 'price', )
    

@admin.register(RequestHealthChecks)
class RequestHealthChecksAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('user', 'exam', 'status', 'required_password', 'result')

@admin.register(SchedulingHealthChecks)
class SchedulingHealthChecksAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'scheduled',)

@admin.register(MedicalAcess)
class MedicalAcessAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('user', 'identifications', 'access_time', 'token')
