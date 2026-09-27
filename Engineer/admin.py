from django.contrib import admin
from .models import EngineerApplication

from .constants import ADMIN_SECTIONS, ADMIN_ACTIONS
@admin.register(EngineerApplication)
class EngineerApplicationAdmin(admin.ModelAdmin):
    # 1. Added 'work_region' to the list display
    list_display = ("full_name_ar", "email", "phone", "city", "status", "years_of_experience", "sce_number", "created_at")

    # 2. Search in text fields (Added work_region code and name)
    search_fields = (
        'full_name_ar',
        'full_name_en',
        'email',
        'phone',
        "years_of_experience",
        "sce_number",
        'secondary_phone',
        'work_region__name', # New: Search by Region Name
        'work_region__region_code' # New: Search by Region Key
    )

    # 3. Filter sidebar (Added work_region)
    list_filter = ("city", "status", "created_at")

    # 4. Organized layout with the new additions
    fieldsets = (
        (
            ADMIN_SECTIONS["PERSONAL"],
            {
                "fields": (
                    "full_name_ar",
                    "full_name_en",
                    "email",
                    "phone",
                    "sce_expiration_date",
                    "years_of_experience",
                     "sce_number",
                    "secondary_phone",
                    "city",
                )
            },
        ),
        # New Section: Banking Details (Grouped digit + file)
        (
            ADMIN_SECTIONS["BANKING"],
            {
                "fields": (
                    "iban_number",
                    "iban_proof",  # New: The PDF file
                    "iban_status",  # New: Status
                    "iban_notes",  # New: Admin comments
                ),
            },
        ),
        (
            ADMIN_SECTIONS["DEGREE"],
            {
                "fields": ("university_degree", "degree_status", "degree_notes"),
            },
        ),
        (
            ADMIN_SECTIONS["SCE"],
            {
                "fields": ("sce_membership", "sce_status", "sce_notes"),
            },
        ),
        (
            ADMIN_SECTIONS["CV"],
            {
                "fields": ("cv_file", "cv_status", "cv_notes"),
            },
        ),
        (
            ADMIN_SECTIONS["EQUIPMENT"],
            {
                "fields": ("equipment_photos", "equipment_status", "equipment_notes"),
            },
        ),
        (
            ADMIN_SECTIONS["FINAL"],
            {
                "fields": ("status",),
            },
        ),
    )

    # 5. Group Actions
    actions = ['approve_engineers', 'suspend_engineers']

    @admin.action(description=ADMIN_ACTIONS["APPROVE"])
    def approve_engineers(self, request, queryset):
        queryset.update(is_active_for_registration=True)

    @admin.action(description=ADMIN_ACTIONS["SUSPEND"])
    def suspend_engineers(self, request, queryset):
        queryset.update(is_active_for_registration=False)

    # 6. Read-only fields
    readonly_fields = ('created_at',)


from django.contrib import admin
from .models import Engineer

from django.contrib import admin
from .models import Engineer


@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    list_display = ("user", "data")
    search_fields = ("user__username", "user__first_name", "user__last_name")


from django.contrib import admin
from .models import Wallet, Engineer


from django.contrib import admin

from django.contrib import admin
from .models import Engineer, Wallet

from django.db import models
from django.db.models import Sum, F, ExpressionWrapper, fields
from django.utils import timezone
import datetime


from django.contrib import admin
from .models import Engineer, Wallet

from django.contrib import admin
from .models import Engineer, Wallet

from django.contrib import admin
from .models import Wallet, WithdrawalLog


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id",)

@admin.register(WithdrawalLog)
class WithdrawalLogAdmin(admin.ModelAdmin):
    list_display = ("amount", "status")
