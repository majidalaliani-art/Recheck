from django.contrib import admin
from .models import *

# InspectionCategory


@admin.register(EmailSystemSettings)
class EmailSystemSettingsAdmin(admin.ModelAdmin):
    # منع إضافة سجل جديد إذا كان هناك سجل موجود فعلاً
    def has_add_permission(self, request):
        if EmailSystemSettings.objects.exists():
            return False
        return True

    # منع الحذف عشان ما يتعطل النظام
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    # This displays the Key and Name as columns in the main list
    # (Key is the code used by the system, Name is for humans)
    list_display = ('code', 'name', 'is_active')

    # Allow searching by both the String Key and the Name
    search_fields = ('code', 'name')

    # Enable a quick filter for active/inactive regions
    list_filter = ('is_active',)

    # Ordering the list by the Key (Alphabetical/Numerical)
    ordering = ('code',)

    # Using fieldsets to organize the entry form
    fieldsets = (
        ('Region Core Configuration', {
            'fields': ('code', 'name', 'lat', 'lng', 'radius',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


'''
@admin.register(ServicePrice)
class ServicePriceAdmin(admin.ModelAdmin):

    list_display = ('kay', 'category_name', 'std_price', 'comp_price')


    search_fields = ('kay', 'category_name')


    ordering = ('kay',)

    fieldsets = (
        ('المفاتيح والتعريفات', {
            'fields': ('kay', 'category_name'),
            'description': 'استخدم الـ Key للبرمجة (مثلاً: villa) والاسم لنوع العقار (مثلاً: فيلا).'
        }),
        ('قائمة الأسعار', {
            'fields': ('std_price', 'comp_price'),
        }),
    )
'''


# from django.contrib import admin
# from .models import ServicePrice

# @admin.register(ServicePrice)
# class ServicePriceAdmin(admin.ModelAdmin):

#     list_display = ('category_name', 'std_price', 'comp_price')

#     readonly_fields = ('kay',)


#     def has_delete_permission(self, request, obj=None):
#         return False

#     def has_add_permission(self, request):
#         return False

#     # 5. تنسيق صفحة التعديل
#     fieldsets = (
#         ('تعديل الأسعار والأسماء', {
#             'fields': ('category_name', 'std_price', 'comp_price'),
#         }),
#         ('معلومات النظام (للقراءة فقط)', {
#             'fields': ('kay',),
#             'classes': ('collapse',),
#         }),
#     )

'''
@admin.register(ServicePrice)
class ServicePriceAdmin(admin.ModelAdmin):
    # الأعمدة اللي تظهر في الجدول
    list_display = ('category_name', 'service_type', 'std_price', 'comp_price')

    # فلتر جانبي عشان يختار "فحص" أو "استشارة" بضغطة زر
    list_filter = ('service_type',)

    readonly_fields = ('kay', 'service_type')
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False

    # تقسيم صفحة التعديل من الداخل
    fieldsets = (
        ('معلومات الخدمة', {
            'fields': ('category_name', 'service_type', 'kay'),
        }),
        ('الأثمان والأسعار', {
            'fields': ('std_price', 'comp_price'),
            'description': 'ملاحظة: لخدمات الاستشارة، عدل السعر العادي فقط واترك الشامل 0.'
        }),
    )
'''

'''
from django.contrib import admin
from .models import ServicePrice

@admin.register(ServicePrice)
class ServicePriceAdmin(admin.ModelAdmin):
    # 1. الجدول الرئيسي
    list_display = ('category_name', 'service_type', 'std_price', 'comp_price')
    list_filter = ('service_type',)

    # 2. أقفال الأمان الأساسية
    def has_delete_permission(self, request, obj=None): return False
    def has_add_permission(self, request): return False

    # 3. إخفاء المفتاح التقني تماماً (kay)
    # وجعل نوع الخدمة (service_type) للقراءة فقط
    readonly_fields = ('service_type',)
    exclude = ('kay',)

    # 4. تقسيم صفحة التعديل لتكون واضحة جداً
    def get_fieldsets(self, request, obj=None):
        # إذا كانت الخدمة استشارة
        if obj and obj.service_type == 'consultation':
            return (
                ('نوع الخدمة (للقراءة فقط)', {
                    'fields': ('service_type',),
                }),
                ('بيانات الاستشارة', {
                    'fields': ('category_name', 'std_price'),
                }),
            )

        # إذا كانت فحص عقار (فيلا، شقة...)
        return (
            ('نوع الخدمة (للقراءة فقط)', {
                'fields': ('service_type',),
            }),
            ('بيانات فحص العقار', {
                'fields': ('category_name', 'std_price', 'comp_price'),
            }),
        )


'''


@admin.register(PropertyPricing)
class PropertyPricingAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "property_name",
        "std_price",
        "comp_price",
        "meter_rate",
        "allowed_duration",
        "is_active",
    )
    list_editable = (
        "std_price",
        "comp_price",
        "meter_rate",
        "allowed_duration",
        "is_active",
    )
    search_fields = ('key', 'property_name')

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


# from django.contrib import admin
# from .models import WorkDay

# @admin.register(WorkDay)
# class WorkDayAdmin(admin.ModelAdmin):
#     list_display = ('day_key', 'day_name', 'start_time', 'end_time', 'total_price', 'is_working')
#     list_editable = ('start_time', 'end_time', 'total_price', 'is_working')  # يتيح التعديل مباشرة من القائمة
#     list_filter = ('is_working',)  # تصفية حسب حالة التفعيل
#     search_fields = ('day_key', 'day_name')  # بحث سريع
#     ordering = ('day_key',)  # ترتيب حسب المفتاح الإنجليزي


from django.contrib import admin
from .models import WorkDay

@admin.register(WorkDay)
class WorkDayAdmin(admin.ModelAdmin):
    list_display = ('number', 'name_en', 'name_ar', 'start_time', 'end_time', 'duration_minutes', 'total_price', 'is_working')
    list_editable = ('start_time', 'end_time', 'duration_minutes', 'total_price', 'is_working')
    list_filter = ('is_working',)
    search_fields = ('name_en', 'name_ar')
    ordering = ('number',)
    readonly_fields = ('number', 'name_en', 'name_ar')


    #def has_add_permission(self, request):
    #     return False
    # def has_delete_permission(self, request, obj=None):
    #     return False


@admin.register(FinancialSettings)
class FinancialSettingsAdmin(admin.ModelAdmin):
    list_display = ('tax_rate', 'company_profit_percent', 'engineer_profit_percent')
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# @admin.register(InspectionCategory)
# class InspectionCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'is_active')
#     search_fields = ('key', 'name')
#     list_filter = ('is_active',)
#     ordering = ('key',)
#     fieldsets = (
#         ('Region Core Configuration', {'fields': ('key', 'name')}),
#         ('Status', {'fields': ('is_active',)}),)


from django.contrib import admin
from .models import InspectionType


@admin.register(InspectionType)
class InspectionTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "key")
    search_fields = ("name", "key")


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percent", "is_active", "created_at")
    readonly_fields = ("code", "created_at")


@admin.register(ContactMethod)
class ContactMethodAdmin(admin.ModelAdmin):
    list_display = ("key", "name", "link")
    search_fields = ("key", "name")


from django.contrib import admin
from .models import PaymentMethod


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "key", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name", "key")
    prepopulated_fields = {"key": ("name",)}


from .models import SystemSettings

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ("key", "enabled", "delay")
    search_fields = ("key",)
