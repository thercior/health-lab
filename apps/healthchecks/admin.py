from django.contrib import admin
from healthchecks.models import TypeHealthChecks, RequestHealthChecks, SchedulingHealthChecks

admin.site.register(TypeHealthChecks)
admin.site.register(RequestHealthChecks)
admin.site.register(SchedulingHealthChecks)