from django.db import models
from django.core.validators import MinValueValidator
from Client.constants import*

from Admin.models import Region,WorkDay
import random,string
from django.db import models
from config import generate_number

from django.db import models
from Admin.models import PropertyPricing, InspectionType,TimeSlot
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from .constants import *
import uuid
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class UserPhone(models.Model):
    public_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
   # id = models.AutoField()
    phone = models.CharField(max_length=15, unique=True, verbose_name="رقم الجوال")
    is_verified = models.BooleanField(default=False, verbose_name="هل تم التحقق؟")
    applied_for_job = models.BooleanField(default=False, verbose_name="حالة التقديم على وظيفة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="وقت التسجيل")
    def __str__(self):
        return self.phone


ORDER_LABELS = {
    "name": "اسم العميل",
    "phone": "رقم الجوال",
    "account_phone": 'قم الجوال المرتبط بالحساب"',
    "coordinate_later": "التنسيق مع المهندس لاحقاً",
    "property_type": "نوع العقار",
    "inspection_type": "نوع الفحص",
    "property_size": "مساحة العقار (م2)",
    "city": "المدينة",
    "neighborhood": "الحي",
    "unit_number": "رقم الوحدة",
    "detailed_title": "العنوان تفصيلا",
    "latitude": "خط العرض",
    "longitude": "خط الطول",
    "location_url": "رابط الموقع (Google Maps)",
    "final_price": "السعر النهائي",
    "status": "الحالة",
    "documents": "المخططات أو الصكوك والمستندات",
    "entrance_image": "صورة العقار",
    "processed": "تمت المعالجة",
}


import random
import string
from django.db import models


def get_upload_path(instance, filename):
    if hasattr(instance, 'entrance_image'):
        sub_folder = 'entrance_image'
    elif hasattr(instance, 'documents'):
        sub_folder = 'documents'
    else:
        sub_folder = 'general'
    return f'orders/{instance.order_id}/{sub_folder}/{filename}'


def generate_order_number():
    return generate_number(model=Order, field_name='order_id')
class Order(models.Model):
    order_id = models.CharField(primary_key=True, max_length=8, default=generate_order_number, editable=False, unique=True)
    client = models.ForeignKey(UserPhone, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    order = models.OneToOneField("Order",on_delete=models.CASCADE,related_name="payment",verbose_name=PAYMENT_LABELS["order"],)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=PAYMENT_LABELS["amount"])
    tax_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name=PAYMENT_LABELS["tax_amount"],)
    net_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name=PAYMENT_LABELS["net_amount"],)
    engineer_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name=PAYMENT_LABELS["engineer_amount"],)
    platform_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name=PAYMENT_LABELS["platform_amount"],)
    status = models.CharField(max_length=20,choices=PAYMENT_STATUS,default="pending",verbose_name=PAYMENT_LABELS["status"],)
    provider = models.CharField(max_length=100, null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    ref = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=PAYMENT_LABELS["created_at"])
    updated_at = models.DateTimeField(auto_now=True, verbose_name=PAYMENT_LABELS["updated_at"])


phone_validator = RegexValidator(regex=r"^\+?\d{9,15}$", message="رقم الجوال غير صحيح")
class VisitDetails(models.Model):
    visit_id = models.CharField(primary_key=True, max_length=8, default=generate_order_number, editable=False, unique=True)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="visitdetails"
    )
    # --- Customer Info ---
    name = models.CharField(max_length=100,verbose_name=ORDER_LABELS['name'])
    phone = models.CharField(max_length=20,verbose_name=ORDER_LABELS['phone'])
    # --- Scheduling ---

    day = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    status = models.CharField(max_length=20,choices=ORDER_STATUS,default='waiting',verbose_name=ORDER_LABELS['status'])
    # --- Property Details ---
    property_type = models.ForeignKey(PropertyPricing, on_delete=models.PROTECT, verbose_name=ORDER_LABELS['property_type'])

    inspection_type = models.ForeignKey(InspectionType,on_delete=models.PROTECT,verbose_name=ORDER_LABELS['inspection_type'],related_name='visits')

    # --- Location & GPS ---
    city = models.ForeignKey(Region, on_delete=models.PROTECT, limit_choices_to={'is_active': True}, verbose_name=ORDER_LABELS['city'])

    neighborhood = models.CharField(max_length=100, verbose_name=ORDER_LABELS["neighborhood"])

    property_size = models.IntegerField(verbose_name=ORDER_LABELS["property_size"])

    engineer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # --- Documents ---
    #documents = models.FileField(upload_to=get_upload_path, null=True, blank=True, verbose_name=ORDER_LABELS["documents"])


class ConsultationDetails(models.Model):
    consultation_id = models.CharField(primary_key=True, max_length=8, default=generate_order_number, editable=False, unique=True)

    order = models.OneToOneField(
        "Order", on_delete=models.CASCADE, related_name="consultations"
    )

    # --- Customer Info ---
    name = models.CharField(max_length=100, verbose_name="الاسم")
    phone = models.CharField(max_length=15, validators=[phone_validator], verbose_name="رقم الجوال")
    summary = models.TextField(verbose_name="وصف الاستشارة")

    # --- Consultation Content ---
    work_day = models.CharField(max_length=20 , null=True, blank=True)
    work_time = models.CharField(max_length=50)
    work_history = models.DateField()

    # --- Assignment ---
    engineer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)

    # --- Status ---
    status = models.CharField(
        max_length=20,
        choices=CONSULTATION_STATUS,
        default="waiting",
    )

    # --- Timing ---
    created_at = models.DateTimeField(auto_now_add=True)


class WalletTransaction(models.Model):
    wallet = models.ForeignKey('Engineer.Wallet', on_delete=models.CASCADE,related_name="transactions")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="الطلب المرتبط")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default="pending")
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name="تاريخ الإلغاء")
    created_at = models.DateTimeField(auto_now_add=True)
