from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
import datetime
from .constants import *
import random,string

class EmailSystemSettings(models.Model):
    # --- إعدادات السيرفر (المواسير) ---
    smtp_host = models.CharField(max_length=100, default='smtp.gmail.com', verbose_name="سيرفر SMTP")
    smtp_port = models.IntegerField(default=587, verbose_name="المنفذ")

    # أهم إضافة: نوع التشفير (عشان ما تلمس الكود أبداً)
    use_tls = models.BooleanField(default=True, verbose_name="استخدام TLS (أمان حديث)")
    use_ssl = models.BooleanField(default=False, verbose_name="استخدام SSL (أمان قديم)")

    # --- بيانات الحساب (المفتاح) ---
    email_user = models.EmailField(verbose_name="إيميل الإرسال")
    email_password = models.CharField(max_length=100, verbose_name="كلمة مرور التطبيق")

    # --- محتوى الرسالة (الرسالة) ---
    email_subject = models.CharField(max_length=200, default="كود التحقق الخاص بك", verbose_name="عنوان الرسالة")
    email_body = models.TextField(verbose_name="نص الرسالة (قبل الكود)")
    company_name = models.CharField(max_length=100, default="نظام فولت", verbose_name="اسم الشركة للتذيل")

    # --- وضع التطوير (أهم شيء الحين) ---
    send_to_console = models.BooleanField(default=True, verbose_name="إرسال للكونسول فقط؟ (للتجربة)")

    class Meta:
        verbose_name = "إعدادات نظام الإيميل الثابتة"
        verbose_name_plural = "إعدادات نظام الإيميل الثابتة"

    def save(self, *args, **kwargs):
        if not self.pk and EmailSystemSettings.objects.exists():
            raise ValidationError('لا يمكنك إضافة أكثر من سجل واحد.')
        return super(EmailSystemSettings, self).save(*args, **kwargs)


class Region(models.Model):
    code = models.CharField(max_length=50, unique=True, primary_key=True, verbose_name="Region Key/Code")
    name = models.CharField(max_length=100, unique=True, verbose_name="Region Name")
    lat = models.FloatField(null=True,blank=True,verbose_name="Latitude")
    lng = models.FloatField(null=True,blank=True,verbose_name="Longitude")
    radius = models.PositiveIntegerField(default=30000, verbose_name="Coverage Radius")
    is_active = models.BooleanField(default=False, verbose_name="Is Active")

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"

    def __str__(self):
        return self.name


# class ServicePrice(models.Model):

#     kay = models.CharField(max_length=20, unique=True)
#     category_name = models.CharField(max_length=50, unique=True, verbose_name="نوع العقار")
#     std_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="سعر الفحص العادي (Standard)")
#     comp_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="سعر الفحص الشامل (Comprehensive)")

#     def __str__(self):
#         return self.category_name

#     class Meta:
#         verbose_name = "أسعار الخدمات"
#         verbose_name_plural = "أسعار الخدمات"


PROPERTY_LABELS = {
    "key": "المفتاح التقني",
    "property_name": "اسم العقار",
    "std_price": "السعر العادي",
    "comp_price": "السعر الشامل",
    "meter_rate": "سعر المتر الإضافي",
    "is_active": "الحالة",
    "allowed_duration": "المدة المسموحة",
    "free_meters": "عدادات مجانية",
}


class PropertyPricing(models.Model):
    key = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=PROPERTY_LABELS["key"],
    )
    property_name = models.CharField(
        max_length=100,
        verbose_name=PROPERTY_LABELS["property_name"],
    )

    std_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=PROPERTY_LABELS["std_price"],
    )

    comp_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=PROPERTY_LABELS["comp_price"],
    )

    meter_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=PROPERTY_LABELS["meter_rate"],
    )
    free_meters = models.IntegerField(
        default=200, verbose_name=PROPERTY_LABELS["free_meters"]
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=PROPERTY_LABELS["is_active"],
    )

    allowed_duration = models.DurationField(
        default=datetime.timedelta(days=2),
        verbose_name=PROPERTY_LABELS["allowed_duration"],
    )
    class Meta:
        verbose_name = "تسعيرة العقارات"
        verbose_name_plural = "تسعيرات العقارات"

    def __str__(self):
        return f"{self.property_name}"


class FinancialSettings(models.Model):
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=15.00, verbose_name="نسبة الضريبة (%)")
    company_profit_percent = models.DecimalField(max_digits=5, decimal_places=2, default=20.00, verbose_name="نسبة أرباح المنشأة من الضريبة (%)")
    engineer_profit_percent = models.DecimalField(max_digits=5, decimal_places=2, default=80.00, verbose_name="نسبة أرباح المهندس من الضريبة (%)")

    class Meta:
        verbose_name = "إعدادات مالية"
        verbose_name_plural = "إعدادات مالية"

    def save(self, *args, **kwargs):
        if not self.pk and FinancialSettings.objects.exists():
            raise ValidationError('لا يمكن إضافة أكثر من سجل واحد للإعدادات المالية.')
        super().save(*args, **kwargs)


class WorkDay(models.Model):
    number = models.PositiveSmallIntegerField(primary_key=True)
    name_en = models.CharField(unique=True, max_length=20, verbose_name="الاسم بالانجليزية",)
    name_ar = models.CharField(unique=True, max_length=20, verbose_name="الاسم بالعربية",)

    duration_minutes = models.IntegerField(default=60)
    start_time = models.TimeField(verbose_name="وقت البدء")
    end_time = models.TimeField(verbose_name="وقت الانتهاء")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="السعر الإجمالي لليوم"
    )
    is_working = models.BooleanField(
        default=True,
        verbose_name="يوم عمل؟",
        help_text="قم بإلغاء التحديد لتعطيل هذا اليوم"
    )

    class Meta:
        verbose_name = "وقت العمل اليومي"
        verbose_name_plural = "أوقات العمل اليومية"
        ordering = ["name_en"]
    def __str__(self):
        return f"{self.number}"


class WorkingDay(models.Model):
    date = models.DateField(unique=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class TimeSlot(models.Model):
    day = models.ForeignKey(
        WorkingDay,
        limit_choices_to={"is_active": True},
        on_delete=models.CASCADE,
        related_name="slots",
    )

    # قمنا بحذف PERIOD_CHOICES وحذف الـ choices من هنا
    period = models.CharField(
        max_length=50,  # زدت الطول قليلاً ليعطيك حرية في الكتابة
        verbose_name="اسم الفترة",
        help_text="اكتب اسم الفترة هنا (مثلاً: الصباح، العصر، إلخ)",
    )

    start_time = models.TimeField(verbose_name="وقت البداية")
    end_time = models.TimeField(verbose_name="وقت النهاية")
    is_booked = models.BooleanField(default=False, verbose_name="هل هي محجوزة؟")

    def __str__(self):
        return f"{self.day} - {self.period}"


# # ==========================================================
# # 1. INSPECTION CATEGORY MODEL
# # Features: Name (for display) + Key (for backend logic)
# class InspectionCategory(models.Model):
#     # "key" is a unique identifier (slug) used for code logic (e.g., 'elec_system')
#     key = models.SlugField(max_length=50, unique=True, verbose_name=MODEL_LABELS['cat_key'])
#     name = models.CharField(max_length=100, verbose_name=MODEL_LABELS['cat_name'])
#     is_active = models.BooleanField(default=True, verbose_name=MODEL_LABELS['cat_active'])
#     def __str__(self):
#         # Shows both for clarity in the Admin panel
#         return f"{self.name}"

# # ==========================================================

class InspectionType(models.Model):
    key = models.SlugField(max_length=50, unique=True, verbose_name="المفتاح (EN)")
    name = models.CharField(max_length=50, verbose_name="الاسم (AR)")
    def __str__(self):
        return self.name


def generate_coupon():
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        if not Coupon.objects.filter(code=code).exists():
            return code
class Coupon(models.Model):
    code = models.CharField(max_length=50,default=generate_coupon,unique=True)
    discount_percent = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ContactMethod(models.Model):
    key = models.SlugField(max_length=50, unique=True, verbose_name="المفتاح")
    name = models.CharField(max_length=50, blank=True, verbose_name="الاسم")
    user = models.CharField(max_length=50, blank=True, verbose_name="اليوزر")
    link = models.CharField(max_length=255, verbose_name="الرابط")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="الأيقونة (اختياري)")
    is_active = models.BooleanField(default=False, verbose_name="Is Active")
    def __str__(self):
        return self.link


class PaymentMethod(models.Model):
    key = models.SlugField(max_length=50, unique=True, verbose_name="المفتاح (كود البوابة)")
    name = models.CharField(max_length=50, verbose_name="اسم وسيلة الدفع")
    is_active = models.BooleanField(default=False, verbose_name="مفعلة / معطلة")

    class Meta:
        verbose_name = "وسيلة دفع"
        verbose_name_plural = "وسائل الدفع"

    def __str__(self):
        return self.key





class SystemSettings(models.Model):
    key = models.CharField(max_length=50, unique=True, primary_key=True, verbose_name="المفتاح")
    name = models.CharField(max_length=50, verbose_name="الاسم")
    enabled = models.BooleanField(
        default=True, verbose_name="تفعيل النشر التلقائي"
    )
    delay = models.PositiveIntegerField(
        default=30, validators=[MinValueValidator(1)], verbose_name="مدة النشر بالدقائق"
    )
