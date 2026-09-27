from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from Admin.models import PropertyPricing
from Client.models import (
    ConsultationDetails,
    Payment,
    VisitDetails,
    WalletTransaction,
)
from Client.utils import get_logged_user
from Visits.models import VisitReport
from config import generate_otp, session_value
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .constants import ENGINEER_PATH as PATH
from .forms import ApplyViewForm, RegisterForm
from .models import Engineer, EngineerApplication, Wallet, WithdrawalLog
from .services.email import send_otp_email
from .tasks import expire_order
from .utils import check_and_compress_file, create_or_reactivate_transaction

User = get_user_model()





class ApplyView(View):
    template_name = PATH["APPLY"]
    readonly_fields = [
        "phone",
        "full_name_ar",
        "full_name_en",
        "secondary_phone",
        "email",
        "iban_number",
        "city",
        "sce_number",
        "years_of_experience",
    ]

    def get(self, request):
        notes = None
        file = None
        phone = get_logged_user(request)
        applicant = EngineerApplication.objects.filter(account=phone).first()
        if applicant:
            form = ApplyViewForm(instance=applicant)
            notes = {
                "degree_notes": applicant.degree_notes,
                "sce_notes": applicant.sce_notes,
                "iban_notes": applicant.iban_notes,
                "cv_notes": applicant.cv_notes,
                "equipment_notes": applicant.equipment_notes,
            }

            file = {
                "degree_status": applicant.degree_status,
                "sce_status": applicant.sce_status,
                "iban_status": applicant.iban_status,
                "cv_status": applicant.cv_status,
                "equipment_status": applicant.equipment_status,
                "status": applicant.status,
            }

            for field in self.readonly_fields:
                if field in form.fields:
                    form.fields[field].widget.attrs["disabled"] = "disabled"

        else:
            phone = phone.phone if phone else None
            form = ApplyViewForm(initial={"phone": phone})
        context = {"form": form, "notes": notes, "file": file}
        return render(request, self.template_name, context)

    def post(self, request):
        phone = get_logged_user(request)
        applicant = EngineerApplication.objects.filter(account=phone).first()

        if applicant and applicant.status == "pending":
            context_errors = {}

            file_mapping = {
                "iban_proof": {
                        "file": "iban_proof",
                        "status": "iban_status",
                        "notes": "iban_notes",
                    },
                "university_degree": {
                        "file": "university_degree",
                        "status": "degree_status",
                        "notes": "degree_notes",
                    },
                "sce_membership": {
                    "file": "sce_membership",
                    "status": "sce_status",
                    "notes": "sce_notes",
                },
                "cv_file": {
                    "file": "cv_file",
                    "status": "cv_status",
                    "notes": "cv_notes",
                },
                "equipment_photos": {
                    "file": "equipment_photos",
                    "status": "equipment_status",
                    "notes": "equipment_notes",
                },
            }

            for file_key, fields in file_mapping.items():
                if file_key in request.FILES:
                    file_value = request.FILES.get(file_key)
                    if file_value:
                        success, result = check_and_compress_file(file_value, file="bdf")
                        if success:
                            setattr(applicant, fields["file"], result)
                            setattr(applicant, fields["notes"], "")
                            setattr(applicant, fields["status"], "required")
                        else:
                            error_map = {
                                "insecure": "تم رفض الملف! يحتوي على برمجيات أو روابط غير آمنة.",
                                "unsupported": "صيغة الملف غير مدعومة.",
                                "invalid_image": "الملف المرفوع ليس صورة صالحة أو تالفة.",
                            }
                            context_errors[f"{file_key}_error"] = error_map.get(
                                result, "حدث خطأ أثناء معالجة الملف."
                            )

            if context_errors:
                form = ApplyViewForm(request.POST, request.FILES, instance=applicant)

                for field in self.readonly_fields:
                    if field in form.fields:
                        form.fields[field].disabled = True
                        current_classes = form.fields[field].widget.attrs.get("class", "")
                        clean_classes = current_classes.replace("error", "").strip()
                        form.fields[field].widget.attrs["class"] = clean_classes

                file = {
                    "degree_status": applicant.degree_status,
                    "sce_status": applicant.sce_status,
                    "iban_status": applicant.iban_status,
                    "cv_status": applicant.cv_status,
                    "equipment_status": applicant.equipment_status,
                    "status": applicant.status,
                }
                context = {"form": form,"notes": context_errors,"file": file,}

                return render(request, self.template_name, context)

            if applicant.status == "pending":
                    applicant.status = "pending"
                    applicant.save()
            return redirect(request.path)
        else:
            form = ApplyViewForm(request.POST, request.FILES)
            context = {"form": form, "notes": None, "file": None}
            if form.is_valid():
                obj = form.save(commit=False)
                obj.account = phone
                obj.save()
            return render(request, self.template_name, context)


class SignUpView(View):
    template_name = PATH["REGISTER"]
    def get(self, request):
        if request.user.is_authenticated :
            return redirect("Staff:staff_data")
        phone = get_logged_user(request)
        if not phone:
           return redirect("Client:login")
        profile = EngineerApplication.objects.filter(account=phone,status='success').first()
        if not profile:
            return redirect("Staff:apply")
        elif hasattr(profile, 'staff_data'):
            return redirect("Admin:login")
        form = RegisterForm(initial={"email": profile.email,})
        return render(request, self.template_name, {"form": form})
    def post(self, request):
        if request.user.is_authenticated :
            return redirect("Staff:staff_data")
        phone = get_logged_user(request)
        if not phone:
            return redirect("Client:login")
        profile = EngineerApplication.objects.filter(account=phone, status='success').first()
        if not profile:
            return redirect("Staff:apply")
        elif hasattr(profile, 'staff_data'):
            return redirect("Admin:login")

        form = RegisterForm(request.POST, initial={"email": profile.email})
        if form.is_valid():
            user = form.save()
            wallet = Wallet.objects.create()
            Engineer.objects.create(user=user,wallet=wallet,data=profile)
            login(request, user)
            return redirect("Staff:staff_data")
        return render(request, self.template_name, {"form": form})




class OrdersOverviewView(LoginRequiredMixin, View):
    template_name = PATH["ORDERS_DISPLAY"]
    def get(self, request):
        current_url_name = request.resolver_match.url_name
        staff = request.user

        Visit = VisitDetails.objects.none()
        Consultation = ConsultationDetails.objects.none()
        is_visit = True
        is_consultation = True



        staff_profile =  getattr(staff, 'staff_profile', None)
        if staff_profile:


            URL_STATUS_MAP = {
                "under_review_orders": "under_review",
                "in_progress_orders": "in_progress",
                "completed_orders": "completed",
            }

            if current_url_name in URL_STATUS_MAP:
                target_status = URL_STATUS_MAP[current_url_name]
                Visit = VisitDetails.objects.filter(status=target_status,engineer=staff).order_by("-order__created_at")
                Consultation = ConsultationDetails.objects.filter(status=target_status,engineer=staff).order_by("-order__created_at")


            elif current_url_name == "available_orders":
                user_groups = staff.groups.values_list("name", flat=True)
                is_visit = "visit" in user_groups
                is_consultation = "consultation" in user_groups
                city = staff_profile.data.city.code
                if staff_profile.is_subscription_active and city:
                    Visit = VisitDetails.objects.filter(status="published", engineer__isnull=True, city__code=city).order_by("-order__created_at")
                    Consultation = ConsultationDetails.objects.filter(status="published", engineer__isnull=True).order_by("-order__created_at")
                else:
                    Visit = VisitDetails.objects.none()
                    Consultation = ConsultationDetails.objects.none()



        return render(request,self.template_name,
            {
                "Visit": Visit,
                "Consultation": Consultation,
                "visit_group": is_visit,
                "consultation_group": is_consultation,
            },
        )
    def post(self, request):
        current_url_name = request.resolver_match.url_name
        staff = request.user
        staff_profile =  getattr(staff, 'staff_profile', None)
        if not staff_profile:
            return redirect(request.path)

        if current_url_name == "available_orders":
            accept = request.POST.get("accept")
            visit_id = request.POST.get("visit_id")
            consultation_id = request.POST.get("consultation_id")
            with transaction.atomic():
                if accept == "Visit":
                    visit = VisitDetails.objects.filter(visit_id=visit_id,engineer__isnull=True,status="published").select_for_update().first()
                    if not visit:
                        return redirect(request.path)
                    pricing = PropertyPricing.objects.filter(key=visit.property_type.key).first()
                    is_visit = staff.groups.filter(name="visit").exists()
                    payment = Payment.objects.filter(order=visit.order).first()
                    if not is_visit or not payment:
                        return redirect(request.path)
                    deadline_duration = (pricing.allowed_duration if pricing and pricing.allowed_duration else timedelta(days=2))
                    visit.start_at = timezone.now()
                    visit.end_at = timezone.now() + deadline_duration
                    visit.engineer = staff
                    visit.status = "in_progress"
                    expire_order.apply_async(args=[visit.visit_id,"visit"],countdown=deadline_duration.total_seconds(),)
                    visit.save()
                    create_or_reactivate_transaction(Order=visit.order,Wallet=staff_profile.wallet,Amount=payment.engineer_amount)
                    return redirect("Staff:in_progress_orders")

                elif accept == "Consultation":
                    consultation = VisitDetails.objects.filter(consultation_id=consultation_id,engineer__isnull=True,status="published").select_for_update().first()

                    if not consultation:
                        return redirect(request.path)
                    is_consultation = staff.groups.filter(name="consultation").exists()
                    payment = Payment.objects.filter(order=consultation.order).first()
                    if not is_consultation or not payment:
                        return redirect(request.path)
                    consultation.engineer = request.user
                    consultation.status = "in_progress"
                    consultation.save()
                    create_or_reactivate_transaction(Order=consultation.order,Wallet=staff_profile.wallet,Amount=payment.engineer_amount)
                    return redirect("Staff:in_progress_orders")
        return redirect(request.path)


class OrderDetailView(LoginRequiredMixin, View):
    template_name = PATH["PROGRESS_ORDER"]

    def get(self, request, type, pk):

        order = None
        start = False
        if type == "visit":
            order = get_object_or_404(VisitDetails, visit_id=pk)
            payment = Payment.objects.filter(order=order.order).first()
            Request = VisitReport.objects.filter(Request=pk).first()


            if not payment :
                return redirect("Staff:available_orders")
            elif Request:
                start = True

            context = {
                "order": order,
                "id": order.visit_id,
                "status_progress": order.get_status_display(),
                "service": "زيارة",
                "key": "visit",
                "date": order.day,
                "time_slot": order.get_time_slot_display,
                "district": order.neighborhood,
                "city": order.city,
                "property": order.property_type,
                "inspection": order.inspection_type,
                "size": order.property_size,
                "price": payment.engineer_amount,
                "deadline": order.end_at,
                "deadline_iso": order.end_at.isoformat(),
                "start": start,
            }

        elif type == "consultation":
            order = get_object_or_404(ConsultationDetails, consultation_id=pk)
            payment = Payment.objects.filter(order=order.order).first()
            if not payment :
                return redirect("Staff:available_orders")




            # elif Request:
            #     start = True

            context = {
                "order": order,
                "id": order.consultation_id,
                "status_progress": "قيد العمل",
                "service": "استشارة",
                "key": "consultation",
                "date": order.work_history,
                "time_slot": order.work_time,
                "day": order.work_day,
                "summary": order.summary,
                "price": payment.engineer_amount,
                "deadline": order.end_at,
                "deadline_iso":None,
                "start": start,
            }

        else:
            return redirect("Staff:in_progress_orders")
        return render(request, self.template_name, {"order": order, "context": context})

    def post(self, request, type, pk):
        action = request.POST.get("action")
        order = None

        if type == "visit":
            order = get_object_or_404(VisitDetails, visit_id=pk)
            if action == "start":
                _, created = VisitReport.objects.get_or_create(Request=order)

                if not created:
                    return redirect(request.path)
                return redirect("operations:visit_detail", pk=pk)




        elif type == "consultation":
            order = get_object_or_404(ConsultationDetails, consultation_id=pk)
        else:
            return redirect(request.path)

        if action == "cancel":
            if not order :
                return redirect(request.path)
            _, created = VisitReport.objects.get_or_create(Request=order)
            if not created:
                return redirect(request.path)
            transaction = WalletTransaction.objects.filter(order=order.order,status="pending").last()
            order.status = "published"
            order.engineer = None
            order.end_at = None
            order.start_at = None
            order.save()
            if transaction:
                transaction.status = "cancel"
                transaction.cancelled_at = timezone.now()
                transaction.save()
            return redirect("Staff:in_progress_orders")

        return redirect(request.path)



class SettingsView(LoginRequiredMixin,View):
    template_name = PATH["SETTINGS"]
    def get(self, request):
        return render(request, self.template_name, {"form": "form"})



class staffDataView(LoginRequiredMixin, View):
    template_name = PATH["DATA"]
    def get(self, request):
        staff = getattr(request.user, 'staff_profile', None)
        data = getattr(staff, 'data', None)
        context={}
        if data :
            context = {
                # البيانات الشخصية والأساسية
                "full_name_ar": data.full_name_ar,
                "full_name_en": data.full_name_en,
                "email": data.email,
                "phone": data.phone,
                "secondary_phone": data.secondary_phone,
                "years_of_experience": data.years_of_experience,
                "city": data.city,
                "sce_number": data.sce_number,
                "sce_expiration_date": data.sce_expiration_date,

                # المستندات والملفات فقط

                "iban_proof": data.iban_proof,
                "university_degree": data.university_degree,
                "sce_membership": data.sce_membership,
                "cv_file": data.cv_file,
                "equipment_photos": data.equipment_photos,
            }
        return render(request, self.template_name, context)



class WalletView(LoginRequiredMixin, View):
    template_name = PATH["WALLET"]
    def get(self, request, *args, **kwargs):
        staff_profile =  getattr(request.user, 'staff_profile', None)

        context = {"wallet": None, "withdrawals": []}
        if staff_profile and hasattr(staff_profile, 'wallet'):
            context = {
                "wallet": staff_profile.wallet.get_wallet_summary(),
                "withdrawals": WithdrawalLog.objects.filter(wallet=staff_profile.wallet).order_by("-created_at"),
            }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        staff_profile =  getattr(request.user, 'staff_profile', None)
        if not staff_profile or not hasattr(staff_profile, 'wallet'):
            return redirect(request.path)
        action = request.POST.get("action")


        if action == "withdraw" and staff_profile:
            withdraw = staff_profile.wallet
            summary = withdraw.get_wallet_summary()
            available_balance = summary.get('available_balance', 0.0)

            if available_balance > 0:
                with transaction.atomic():
                    withdraw.transactions.filter(status="completed").update(status="withdraw")
                    WithdrawalLog.objects.create(wallet=withdraw,amount=available_balance,status="success",message="تم طلب السحب بنجاح",)
        return redirect(request.path)
