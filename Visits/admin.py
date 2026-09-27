from django.contrib import admin
from .models import VisitReport


@admin.register(VisitReport)
class VisitReportAdmin(admin.ModelAdmin):
    list_display = ("Request", "property_condition", "neighborhood", "date", "time")
    search_fields = ("Request__id", "neighborhood", "property_owner")
    list_filter = ("property_condition", "date", "time")
