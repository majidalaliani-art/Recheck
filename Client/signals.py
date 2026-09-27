# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from Client.models import Order
# from django.utils import timezone
# from Admin.models import PropertyPricing
# from Client.utils import get_financial_settings
# from django.contrib.auth.models import Group
# from .models import Order
# from Visits.models import PropertyInfo,FieldVisit


# @receiver(post_save, sender=Order)
# def notify_engineers_new_order(sender, instance, created, **kwargs):
#     if created:
#         try:
#             tax_rate, company_share, engineer_share = get_financial_settings()
#             base_price = instance.final_price
#             tax_amount = base_price * (tax_rate / 100)
#             price_after_tax = base_price - tax_amount
#             company_amount = price_after_tax * (company_share / 100)
#             engineer_amount = price_after_tax * (engineer_share / 100)
#             FieldVisit.objects.create(
#                 order=instance,
#                 total_amount=price_after_tax,
#                 total_with_tax=base_price,
#                 engineer_amount=engineer_amount,
#                 platform_amount=company_amount,
#                 tax_rate_amount=tax_amount,
#                 engineer=None,
#             )
#         except Exception as e:
#             print(e)


# @receiver(post_save, sender=PropertyInfo)
# def sync_status_to_order(sender, instance, **kwargs):
#     if instance.field_visit.order.property_size != instance.building_area_sqm:
#         instance.field_visit.order.property_size = instance.building_area_sqm
#         instance.field_visit.order.save()


from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from Admin.models import PropertyPricing, WorkDay, ContactMethod, Region, PaymentMethod, SystemSettings

from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import VisitDetails, ConsultationDetails, Payment

from datetime import datetime
from django.utils import timezone

from .tasks import publish_order
from django.db.models.signals import pre_save
# from Engineer.services.telegram.send_telegram_message import
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(post_save, sender=PropertyPricing)
def client_visit_card(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "global",
        {
            "type": "global_update",
            "data": {
                "type": "client_visit_card",
                "key": instance.key,
                "free": str(int(instance.free_meters)),
                "std": str(int(instance.std_price)),
                "comp": str(int(instance.comp_price)),
                "meter": str(int(instance.meter_rate)),
            },
        },
    )


@receiver(post_save, sender=WorkDay)
def client_consultation_card(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    current_day = timezone.now().strftime("%A").lower()
    instance_day = instance.name_en.lower()
    if instance_day != current_day:
        return
    async_to_sync(channel_layer.group_send)(
        "global",
        {
            "type": "global_update",
            "data": {
                "type": "client_consultation_card",
                "price": str(int(instance.total_price)),
                "duration": str(int(instance.duration_minutes)),
            },
        },
    )


@receiver(post_save, sender=ContactMethod)
def contact_method_changed(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "global",
        {
            "type": "global_update",
            "data": {
                "type": "contact_method",
                "key": instance.key,
                "link": instance.link,
                "user": instance.user,
                "is_active": instance.is_active,
            },
        },
    )


@receiver(post_save, sender=PaymentMethod)
def payment_method_changed(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "global",
        {
            "type": "global_update",
            "data": {
                "type": "payment_method",
                "key": instance.key,
                "is_active": instance.is_active,
            },
        },
    )


@receiver(pre_save, sender=Region)
def city_changed(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    old = Region.objects.filter(pk=instance.pk).values("is_active", "name").first()
    if old is None:
        return

    if old == {"is_active": instance.is_active, "name": instance.name}:
        return

    async_to_sync(channel_layer.group_send)(
        "global",
        {
            "type": "global_update",
            "data": {
                "type": "city_toggle",
                "code": instance.code,
                "name": instance.name,
                "is_active": instance.is_active,
            },
        },
    )


@receiver(post_save, sender=VisitDetails)
def visit_status_changed(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    data = {}
    status_class = None
    status_text = None

    if instance.order.payment.status == "success":
        status_class = instance.status,
        status_text = instance.get_status_display(),
    else:
        status_class = instance.order.payment.status,
        status_text = instance.order.payment.get_status_display()
    if created:
        data = {
            "type": "visit_status_new",
            "id": str(instance.order.order_id),
            "status_class": status_class,
            "status_text": status_text,
            "neighborhood": instance.neighborhood,
            "city": instance.city.name,
            "property_size": instance.property_size,
            "property_type": instance.property_type.property_name,
            "inspection_type": instance.inspection_type.name,
            "day": instance.day.strftime("%Y-%m-%d"),
            "price": str(int(instance.order.payment.amount)),
            "time_slot": instance.get_time_slot_display(),
        }
    else:
        data = {
            "type": "order_status_updated",
            "id": str(instance.order.order_id),
            "status_class": status_class,
            "status_text": status_text,

        }

    async_to_sync(channel_layer.group_send)(
        f"client_{instance.order.client.phone}",
        {
            "type": "client_update",
            "data": data,
        },
    )


@receiver(post_save, sender=ConsultationDetails)
def consultation_status_changed(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    data = {}
    status_class = None
    status_text = None

    if instance.order.payment.status == "success":
        status_class = (instance.status,)
        status_text = instance.get_status_display(),

    else:
        status_class = (instance.order.payment.status,)
        status_text = instance.order.payment.get_status_display()

    if created:
        data = {
            "type": "consultation_status_new",
            "id": str(instance.order.order_id),
            "work_history": instance.work_history.strftime("%Y-%m-%d"),
            "work_time": instance.work_time,
            "price": str(int(instance.order.payment.amount)),
            "status_text": status_text,
            "status_class": status_class,
        }
    else:
        data = {
            "type": "order_status_updated",
            "id": str(instance.order.order_id),
            "status_class": status_text,
            "status_text": status_class,
        }

    if instance.engineer:
        data["engineer"] = {
            "name": instance.engineer.first_name,
            "phone": instance.engineer.staff_profile.data.phone,
        }

    async_to_sync(channel_layer.group_send)(
        f"client_{instance.order.client.phone}",
        {
            "type": "client_update",
            "data": data,
        },
    )


@receiver(post_save, sender=Payment)
def payment_status_changed(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    if instance.status == "success":
        order = instance.order
        detail_obj = None
        settings_key = ""
        model_class = None
        detail_id = None
        if hasattr(order, 'visitdetails'):
            detail_obj = order.visitdetails
            settings_key = "visit"
            detail_id = detail_obj.visit_id
            model_class = VisitDetails
            print(model_class)
        # if instance.order.visitdetails.status == "waiting":
        #     settings = SystemSettings.objects.filter(key="visit").first()
        #     enabled = settings.enabled if settings else False
        #     if enabled:
        #         publish_order.apply_async(
        #             args=[instance.order.visitdetails.visit_id, VisitDetails],
        #             countdown=settings.delay * 60,
        #         )
        #     else:
        #         instance.order.visitdetails.status = "published"
        #         instance.order.visitdetails.save()

    async_to_sync(channel_layer.group_send)(
        f"client_{instance.order.client.phone}",
        {
            "type": "client_update",
            "data": {
                "type": "​notify_application_status",
                "id": instance.order.order_id,
                "status_class": instance.status,
                "status_text": instance.get_status_display(),
            },
        },
    )
