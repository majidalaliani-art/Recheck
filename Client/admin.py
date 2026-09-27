from django.contrib import admin
from .models import *


# =========================
# Visit Inline (OneToOne with Order)
# =========================
class VisitDetailsInline(admin.StackedInline):
    model = VisitDetails
    extra = 0
    max_num = 1
    can_delete = False


# =========================
# Consultation Inline (OneToOne with Order)
# =========================
class ConsultationDetailsInline(admin.StackedInline):
    model = ConsultationDetails
    extra = 0
    max_num = 1
    can_delete = False


# =========================
# Order Admin (Main model)
# =========================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "client", "order_type", "created_at")
    list_filter = ("order_type",)
    search_fields = ("order_id", "client__phone")

    # Show inline based on order type
    def get_inlines(self, request, obj=None):
        if obj:
            if obj.order_type == "visit":
                return [VisitDetailsInline]
            if obj.order_type == "consultation":
                return [ConsultationDetailsInline]
        return []


# =========================
# Visit Details Admin
# =========================
@admin.register(VisitDetails)
class VisitDetailsAdmin(admin.ModelAdmin):
    list_display = ("order", "name", "city", "property_type", "status",)
    list_filter = ("city", "property_type", "status")
    search_fields = ("name", "phone", "order__order_id")


# =========================
# Consultation Details Admin
# =========================
@admin.register(ConsultationDetails)
class ConsultationDetailsAdmin(admin.ModelAdmin):
    list_display = ("order", "name", "phone", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "phone", "order__order_id")


# =========================
# Wallet Transactions Admin
# =========================
@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ("order", "wallet", "amount", "status", "created_at")
    list_filter = ("status", "wallet")
    search_fields = ("order__order_id", "engineer__id")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_filter = ("status",)


@admin.register(UserPhone)
class UserPhoneAdmin(admin.ModelAdmin):
    list_display = ("public_id", "phone", "is_verified", "created_at")
    list_display_links = ("public_id", "phone")
    search_fields = ("phone",)
    list_filter = ("is_verified", "created_at")
    ordering = ("-created_at",)
