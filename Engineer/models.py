from django.db import models
from django.core.validators import RegexValidator,MinLengthValidator
from django.utils import timezone
import uuid
from .constants import *
# from localflavor.ar.forms import
from Admin.models import Region

import uuid
from django.db import models

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from Client.models import UserPhone
from django.utils import timezone
from datetime import timedelta


from django.utils import timezone
from datetime import timedelta


from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta


import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User


from django.core.validators import FileExtensionValidator, RegexValidator

from django.utils import timezone

def engineer_directory_path(instance, filename):

    now = timezone.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')

    # 2. تحديد نوع المجلد بناءً على الامتداد
    ext = filename.split('.')[-1].lower()
    if ext in ['pdf', 'doc', 'docx']:
        folder_type = 'documents_pdf'
    elif ext in ['jpg', 'jpeg', 'png']:
        folder_type = 'images'
    else:
        folder_type = 'others'

    return f'engineers/{instance.username}/{year}/{month}/{day}/{folder_type}/{filename}'


phone_validator = RegexValidator(
    regex=r"^[+]?[0-9]+$",
    message="خطأ: يجب أن يحتوي الحقل على أرقام فقط، ويمكن أن يبدأ بعلامة + أو * في أول النص فقط.",
)


import os
import shutil
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# def folder_path(instance, file, filename):
#     Id = instance.account.public_id
#     folder_path = os.path.join(settings.MEDIA_ROOT, "Profile", Id ,file)
#     if os.path.exists(folder_path):
#         # shutil.rmtree(folder_path)
#         os.makedirs(folder_path)

#     return f"profile/{file}/{Id}/{filename}"


# class DynamicPathUploader:
#     def __init__(self, file):
#         self.file = file
#     def __call__(self, instance, filename):
#         Id = instance.account.public_id
#         folder_path = os.path.join(settings.MEDIA_ROOT, "Profile", Id, self.file)
#         if os.path.exists(folder_path):
#             os.makedirs(folder_path)

#         return os.path.join("Profile", Id, self.file, filename)


class DynamicPathUploader:

    def __init__(self, file):
        self.file = file

    def __call__(self, instance, filename):
        try:
            Id = str(instance.account.public_id)
        except AttributeError:
            Id = str(instance.data.account.public_id)


        folder_path = os.path.join(settings.MEDIA_ROOT,'Staff',Id, "Profile", self.file)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        return os.path.join("Staff", Id, "Profile", self.file, filename)

    def deconstruct(self):
        return (
            f"{self.__module__}.{self.__class__.__name__}",
            [self.file],
            {},
        )


from django.db import models
from django.db.models import Sum


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    def get_wallet_summary(self):
        # 1. المبالغ المكتملة والمتاحة حالياً
        completed_amount = self.transactions.filter(
            status="completed"
        ).aggregate(total=Sum("amount"))["total"] or 0

        # 2. المبالغ التي تم سحبها سابقاً
        withdrawn_amount = self.transactions.filter(
            status="withdraw"
        ).aggregate(total=Sum("amount"))["total"] or 0

        # 3. الرصيد المعلق (الطلبات قيد العمل)
        pending_balance = self.transactions.filter(
            status="pending"
        ).aggregate(total=Sum("amount"))["total"] or 0

        # --------------------------------------------------
        # الحسبات النهائية للكروت الثلاثة:
        # --------------------------------------------------

        # إجمالي الرصيد التاريخي = المكتمل + المسحوب
        # total_earnings = completed_amount + withdrawn_amount

        # الرصيد المتاح للسحب حالياً = المكتمل فقط
        #   available_balance = completed_amount

        return {
            "total_earnings": round(float(completed_amount + withdrawn_amount), 2),
            "pending_balance": round(float(pending_balance), 2),
            "available_balance": round(float(completed_amount), 2),
        }


class EngineerApplication(models.Model):

    account = models.ForeignKey(UserPhone, on_delete=models.CASCADE,related_name="staff_profile",verbose_name="الحساب المرتبط")

    # --- Personal & Contact Information (Original Fields) ---
    full_name_ar = models.CharField(max_length=100, verbose_name=MODEL_LABELS["FULL_NAME_AR"], validators=[RegexValidator(regex=r'^[\u0600-\u06FF\s]+$')])
    full_name_en = models.CharField(max_length=100, verbose_name=MODEL_LABELS["FULL_NAME_EN"], validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$')])
    email = models.EmailField(unique=True, verbose_name=MODEL_LABELS["EMAIL"])
       # 1. رقم عضوية هيئة المهندسين
    sce_number = models.CharField(max_length=50,verbose_name="رقم عضوية هيئة المهندسين")
    years_of_experience = models.PositiveIntegerField(verbose_name="عدد سنوات الخبرة" ,validators=[MinValueValidator(1), MaxValueValidator(80)])
    phone = models.CharField(max_length=20,validators=[phone_validator],verbose_name=MODEL_LABELS["PHONE"])
    secondary_phone = models.CharField(max_length=20,blank=True, null=True, validators=[phone_validator],verbose_name=MODEL_LABELS["SECONDARY_PHONE"])


    # Linking by 'code' to the Region model

    city = models.ForeignKey(Region, on_delete=models.PROTECT, limit_choices_to={'is_active': True}, verbose_name=MODEL_LABELS["CITY"])
    # --- Banking Information (Added IBAN Proof PDF) ---
    iban_number = models.CharField(max_length=35, verbose_name=MODEL_LABELS["IBAN"])
    iban_proof = models.FileField(
        upload_to=DynamicPathUploader(file="ibans"),
        verbose_name="إثبات الآيبان (PDF)",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    iban_status = models.CharField(max_length=20,choices=FILE_STATUS_CHOICES, default='required', verbose_name=f"{MODEL_LABELS['STATUS']} {MODEL_LABELS['IBAN']}")
    iban_notes = models.CharField(max_length=255, blank=True, null=True, verbose_name=f"{MODEL_LABELS['NOTES']} {MODEL_LABELS['IBAN']}")

    # --- Location (Original City + New Linked Region) ---

    # --- Attachments and Statuses (All Unified to PDF) ---

    # 1. University Degree
    university_degree = models.FileField(
        upload_to=DynamicPathUploader(file="degrees"),
        verbose_name=MODEL_LABELS["DEGREE"],
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    degree_status = models.CharField(max_length=20, choices=FILE_STATUS_CHOICES, default='required', verbose_name=f"{MODEL_LABELS['STATUS']} {MODEL_LABELS['DEGREE']}")
    degree_notes = models.CharField(max_length=255, blank=True, null=True, verbose_name=f"{MODEL_LABELS['NOTES']} {MODEL_LABELS['DEGREE']}")

    # 2. SCE Membership

    sce_membership = models.FileField(
        upload_to=DynamicPathUploader(file="sce"),
        verbose_name=MODEL_LABELS["SCE"],
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    sce_status = models.CharField(max_length=20, choices=FILE_STATUS_CHOICES, default='required', verbose_name=f"{MODEL_LABELS['STATUS']} {MODEL_LABELS['SCE']}")
    sce_notes = models.CharField(max_length=255, blank=True, null=True, verbose_name=f"{MODEL_LABELS['NOTES']} {MODEL_LABELS['SCE']}")

    # 3. CV/Resume

    cv_file = models.FileField(
        upload_to=DynamicPathUploader(file="cvs"),
        verbose_name=MODEL_LABELS["CV"],
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )

    cv_status = models.CharField(max_length=20, choices=FILE_STATUS_CHOICES, default='required', verbose_name=f"{MODEL_LABELS['STATUS']} {MODEL_LABELS['CV']}")
    cv_notes = models.CharField(max_length=255, blank=True, null=True, verbose_name=f"{MODEL_LABELS['NOTES']} {MODEL_LABELS['CV']}")

    # 4. Equipment Photos (Now PDF Only as requested)

    equipment_photos = models.FileField(
        upload_to=DynamicPathUploader(file="equipment"),
        verbose_name=MODEL_LABELS["EQUIPMENT"],
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    equipment_status = models.CharField(max_length=20, choices=FILE_STATUS_CHOICES, default='required', verbose_name=f"{MODEL_LABELS['STATUS']} {MODEL_LABELS['EQUIPMENT']}")
    equipment_notes = models.CharField(max_length=255, blank=True, null=True, verbose_name=f"{MODEL_LABELS['NOTES']} {MODEL_LABELS['EQUIPMENT']}")

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="pending",verbose_name="حالة الطلب",)



    # 2. تاريخ انتهاء عضوية الهيئة
    sce_expiration_date = models.DateField(blank=True,null=True,verbose_name="تاريخ انتهاء عضوية الهيئة")


    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.full_name_ar} | {self.phone}"



class Engineer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE, related_name="wallet")

    avatar = models.FileField(
        upload_to=DynamicPathUploader(file="avatar"),
        blank=True,
        null=True,
        verbose_name=MODEL_LABELS["AVATAR"],
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])
        ],
    )


    # ... الدوال والـ Summary حقك ...


    data = models.OneToOneField(EngineerApplication, on_delete=models.CASCADE, related_name='staff_data')



    @property
    def is_subscription_active(self):
        from django.utils import timezone
        if not (self.user and self.user.is_active):
            return False

        if self.data and self.data.sce_number and self.data.sce_expiration_date :
            return timezone.now().date() <= self.data.sce_expiration_date
        return False
    def __str__(self):
        return f"{self.data.account.public_id}"









class WithdrawalLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name='withdrawals')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="success")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def reference_number(self):
        return f"PAY-{self.id:05d}"
