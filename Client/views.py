from django.views import View
from django.shortcuts import render, redirect
from .models import UserPhone, Order, Payment
from django.http import JsonResponse
from config import session_value, generate_otp
from .constants import PATH, LOCK_TIME
import time
from django.core.cache import cache

from .forms import VisitDetailsForm, PhoneForm, ConsultationForm
from django.shortcuts import get_object_or_404

from decimal import Decimal

from django.views import View
from django.shortcuts import get_object_or_404, redirect

from django.conf import settings

from django.http import HttpResponse


from django.utils.http import urlencode


from django.shortcuts import redirect, render


from Admin.models import PropertyPricing, WorkDay, InspectionType, ContactMethod, Region

from django.contrib.auth.models import Group

import json


from django.contrib.auth import login
from django.http import Http404

from datetime import datetime
from .services.payments import create_checkout_session, create_payment_intent
from .services.sms import send_sms
from .services.pricing import create_order


from django.shortcuts import get_object_or_404, redirect

from django.contrib import messages
from django.shortcuts import redirect
from .utils import (
    get_financial_settings,
    calculate_inspection_price,
    get_address_from_coords,
    get_logged_user,
)
from django.http import JsonResponse
from itertools import chain
from datetime import datetime

from django.http import HttpResponseBadRequest


class LoginView(View):
    template_name = PATH["LOGIN"]

    # ================= GET =================
    def get(self, request):
        session_value(request, key="user", value="0500000000")

        if session_value(request, key="user"):
            return redirect("/")

        form = PhoneForm()
        return render(request, self.template_name, {"form": form, "step": "send"})

    # ================= POST =================
    def post(self, request):

        action = request.POST.get("send")
        form = PhoneForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form, "step": "send"})

        phone = form.cleaned_data["phone"]
        cache_key = f"otp:{phone}"
        block_key = f"otp_block:{phone}"

        if session_value(request, key="user", check=phone):
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "step": "send",
                    "error": "This phone number is already logged in on this device",
                },
            )
        # ================= SEND OTP =================
        if action == "send_otp":
            if cache.get(cache_key):
                return render(
                    request,
                    self.template_name,
                    {
                        "form": form,
                        "step": "verify",
                        "error": "Please wait before requesting another code.",
                    },
                )

            otp = generate_otp()
            cache.set(cache_key, otp, 300)
            cache.set(block_key, True, 60)
            send_sms(phone, otp)
            return render(
                request,
                self.template_name,
                {"form": form, "step": "verify", "phone": phone},
            )

        # ================= VERIFY OTP =================
        elif action == "verify_otp":

            input_otp = request.POST.get("otp")
            print(input_otp)
            saved_otp = cache.get(cache_key)
            if not saved_otp:
                return render(
                    request,
                    self.template_name,
                    {
                        "form": form,
                        "step": "send_otp",
                        "phone": phone,
                        "error": "انتهت صلاحية الكود",
                    },
                )

            if input_otp != saved_otp:
                return render(
                    request,
                    self.template_name,
                    {
                        "form": form,
                        "step": "verify",
                        "phone": phone,
                        "error": "الكود غير صحيح",
                    },
                )

            cache.delete(cache_key)

            UserPhone.objects.get_or_create(phone=phone)
            session_value(request, key="user", value=phone)
            app = request.GET.get("app")
            next_page = request.GET.get("next")
            # if next_page and app:
            #     next_page = next_page.strip("/")
            #     page = app + ":" + next_page
            #     return redirect(page)
            return redirect('/')

        # ================= RESET =================
        elif action == "reset":

            if cache.get(block_key):
                return render(
                    request,
                    self.template_name,
                    {
                        "form": form,
                        "step": "verify",
                        "phone": phone,
                        "error": "انتظر قليلاً قبل إعادة الإرسال",
                    },
                )

            otp = generate_otp()

            cache.set(cache_key, otp, 300)
            cache.set(block_key, True, 60)

            send_sms(phone, otp)

            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "step": "verify",
                    "phone": phone,
                    "time_left": block_key,
                    "start_timer": True,
                },
            )

        # ================= FALLBACK (IMPORTANT) =================
        return render(request, self.template_name, {"form": form, "step": "send"})


class HomepageView(View):
    template_name = PATH["HOMEPAGE"]

    def get(self, request):
        visit = PropertyPricing.objects.filter().values(
            "key",
            "std_price",
            "free_meters",
        )
        data_list = list(visit)
        today = datetime.now().strftime("%A").lower()
        WhatsApp = (
            ContactMethod.objects.filter(key="WhatsApp")
            .values_list("link", flat=True)
            .first()
        )
        consultation = (
            WorkDay.objects.filter(name_en=today)
            .values("total_price", "duration_minutes")
            .first()
        )
        data_list += [
            {
                "key": "consultation",
                "total_price": consultation["total_price"] if consultation else None,
                "duration_minutes": (
                    consultation["duration_minutes"] if consultation else None
                ),
            },
            {"key": "others", "whatsapp": WhatsApp},
        ]

        cities = list(
            Region.objects.filter(
                is_active=True,
                lat__isnull=False,
                lng__isnull=False,
            ).values("code", "name", "lat", "lng", "radius", "is_active")
        )

        context = {"services": data_list, "cities_json": json.dumps(cities)}

        return render(request, self.template_name, context)


class ConsultationView(View):
    template_name = PATH["CONSULTATION"]

    def get(self, request):
        phone = session_value(request, key="user") or ""
        form = ConsultationForm(initial={"phone": phone})
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ConsultationForm(request.POST)
        user = get_logged_user(request)
        if not user:
            return redirect("Client:login")
        elif form.is_valid():
            price = form.cleaned_data["price"]

            session_key = request.session.session_key
            key = f"order_lock_{session_key}"
            last = cache.get(key)
            now = time.time()
            if last and now - last < LOCK_TIME:
                return HttpResponse(status=204)
            cache.set(key, now, timeout=LOCK_TIME)
            order = create_order(user, "consultation", int(price))
            consultation = form.save(commit=False)
            consultation.order = order
            consultation.save()
            return redirect("Client:order", order_id=order.order_id)
        return render(request, self.template_name, {"form": form})


class BookingView(View):
    template_name = PATH["BOOKING"]

    def get(self, request):
        phone = session_value(request, key="user") or ""
        form = VisitDetailsForm(initial={"phone": phone})
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = VisitDetailsForm(request.POST)
        user = get_logged_user(request)
        if not user:
            return redirect("Client:login")
        elif form.is_valid():
            user_key = user.pk
            key = f"order_lock_{user_key}"
            last = cache.get(key)
            now = time.time()
            if last and now - last < LOCK_TIME:
                return HttpResponse(status=204)
            cache.set(key, now, timeout=LOCK_TIME)
            property_key = form.cleaned_data["property_type"].key
            inspection_key = form.cleaned_data["inspection_type"].key
            property = get_object_or_404(PropertyPricing, key=property_key)
            inspection = get_object_or_404(InspectionType, key=inspection_key)
            extra = form.cleaned_data["property_size"]
            price = 0
            if inspection.key == "standard":
                price = property.std_price + extra * property.meter_rate
            elif inspection.key == "complete":
                price = property.comp_price + extra * property.meter_rate
            else:
                return HttpResponseBadRequest()

            order = create_order(user, "visit", int(price))
            visit = form.save(commit=False)
            visit.order = order
            visit.save()
            return redirect("Client:order", order_id=order.order_id)
        return render(request, self.template_name, {"form": form})





class OrdersView(View):
    template_name = PATH["ORDERS"]

    def get(self, request):
        client = get_logged_user(request)
        if not client:
            return redirect("Client:login")
        orders = Order.objects.filter(client=client).order_by("-created_at")

        context = {
            "orders": orders,
        }

        if not orders.exists():
            context["message"] = "لا يوجد طلبات"
        return render(request, self.template_name, context)


class OrderView(View):
    template_name = PATH["ORDER"]

    def get(self, request, order_id):
        order = get_object_or_404(Order, order_id=order_id)
        status = None
        Customer = None
        Types = None

        if order.payment.status == "success":
            if hasattr(order, "visitdetails"):
                status = {
                    "en": order.visitdetails.status,
                    "ar": order.visitdetails.get_status_display(),
                }
            elif hasattr(order, "consultation"):
                status = {
                    "en": order.consultation.status,
                    "ar": order.consultation.get_status_display(),
                }
        else:
            status = {
                "en": order.payment.status,
                "ar": order.payment.get_status_display(),
            }

        if order.order_type == "consultation":
            consultation = order.consultations
            Customer = {
                "name": consultation.name,
                "phone": consultation.phone,
                "service": order.get_order_type_display,
            }

            Types = {
                "key": "consultation",
                "date": consultation.work_history,
                "time_slot": consultation.work_time,
                "day": consultation.work_day,
                "summary": consultation.summary,
            }

        elif order.order_type == "visit":
            visitdetails = order.visitdetails
            Customer = {
                "name": visitdetails.name,
                "phone": visitdetails.phone,
                "service": order.get_order_type_display,
            }

            Types = {
                "key": "visit",
                "date": visitdetails.day,
                "time_slot": visitdetails.get_time_slot_display,
                "district": visitdetails.neighborhood,
                "city": visitdetails.city,
                "property": visitdetails.property_type,
                "inspection": visitdetails.inspection_type,
                "size": visitdetails.property_size,
            }

        context = {
            "id": order.order_id,
            "status": status,
            "Customer": Customer,
            "Types": Types,
            "price": order.payment.amount,
        }

        return render(request, self.template_name, context)

    def post(self, request, order_id):
        if request.method == "POST":
            orders_list = get_object_or_404(Order, order_id=order_id)
            action = request.POST.get("action")
            if action == "cancel" and orders_list.payment:
                orders_list.payment.status = "cancel"
                orders_list.payment.save()
            elif action == "failed":
                orders_list.payment.status = "pending"
                orders_list.payment.save()
        return redirect(request.path)