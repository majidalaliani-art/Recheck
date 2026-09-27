# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# import json


# import threading
# import time
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from Visits.models import FieldVisit


# import threading
# import time

# import json
# import threading
# import time

# import logging

# # إعداد اللوجر (تأكد إنه شغال في settings.py)
# logger = logging.getLogger(__name__)

# import threading
# import logging
# from django.utils import timezone

# logger = logging.getLogger(__name__)


# def wait_and_activate(visit_id):
#     try:
#       time.sleep(5)
#       visit = FieldVisit.objects.get(pk=visit_id)
#       if visit.status == "null":
#         visit.status = "pending"
#         visit.save()
#     except Exception as e:
#         logger.error(f"❌ Critical Error in wait_and_activate for {visit_id}: {str(e)}")


# def delete_request(instance):
#     channel_layer = get_channel_layer()
#     group_name = str(instance.order.city.code).lower()
#     async_to_sync(channel_layer.group_send)(
#         group_name,
#         {"type": "remove_order_notification", "order_id": instance.pk},
#     )


# @receiver(post_save, sender=FieldVisit)
# def notify_engineers_on_status_change(sender, instance, created, **kwargs):
#     if instance.status == "null":
#         if not created:
#             delete_request(instance)
#             pass

#         thread = threading.Thread(target=wait_and_activate, args=(instance.pk,))
#         thread.start()

#     elif instance.status == "pending":
#         channel_layer = get_channel_layer()
#         order_payload = {
#             "type": "new_order",
#             "id": instance.pk,
#             "title": "q",
#             "city": "جدة",
#             "price": "1",
#         }

#         group_name = str(instance.order.city.code).lower()
#         async_to_sync(channel_layer.group_send)(
#             group_name,
#             {"type": "send_order_notification", "order_data": order_payload},
#         )


# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.utils import timezone

# from datetime import timedelta
# from .tasks import send_wallet_update_task


# from django.utils import timezone
# from core.celery import app
# from .tasks import send_wallet_update_task

# import uuid
# from django.utils import timezone
# from django.db.models.signals import pre_save
# from django.dispatch import receiver


# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer

# from django.db import transaction
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# import uuid
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.conf import settings

# @receiver(pre_save, sender=FieldVisit)
# def smart_financial_logic(sender, instance, **kwargs):

#     if instance.paid_at:
#         return

#     if instance.wallet and instance.processed:
#         # old = sender.objects.filter(pk=instance.pk).first()
#         # if old.holding_days == instance.holding_days:
#         #     return

#         if instance.current_task_id:
#             app.control.revoke(instance.current_task_id, terminate=True)

#         new_unique_id = f"wallet_v{instance.visit_id}_{uuid.uuid4().hex[:8]}"
#         instance.current_task_id = new_unique_id

#         send_wallet_update_task.apply_async(
#             args=[instance._meta.app_label, instance._meta.model_name, instance.pk],
#             countdown=int(instance.holding_days) * 86400,
#             task_id=new_unique_id,
#         )

#     else:
#         if instance.financial_approved_at is not None:
#             instance.financial_approved_at = None

#         if instance.current_task_id:
#             app.control.revoke(instance.current_task_id, terminate=True)
#             instance.current_task_id = None


# @receiver(post_save, sender=FieldVisit)
# def update_engineer_live_ui(sender, instance, **kwargs):

#     def send_data():
#         engineer = instance.engineer
#         wallet_obj = engineer.user.wallet
#         channel_layer = get_channel_layer()
#         room_group_name = f"engineer_{engineer.user.id}"
#         new_numbers = {
#             "total": float(wallet_obj.get_total_earnings(FieldVisit)),
#             "frozen": float(wallet_obj.get_pending_balance(FieldVisit)),
#             "withdrawable": float(wallet_obj.get_withdrawable_balance(FieldVisit)),
#         }
#         async_to_sync(channel_layer.group_send)(
#                 room_group_name,
#                 {
#                     "type": "wallet_update_event",
#                     "numbers": new_numbers
#                 }
#             )

#     transaction.on_commit(send_data)


# from .models import EngineerApplication
# @receiver(post_save, sender=EngineerApplication)
# def notify_application_status(sender, instance, created, **kwargs):
#     channel_layer = get_channel_layer()

#     # if created:
#     #     return

#     # if instance.status == "accepted" or instance.status == "rejected":
#         # subject = "تحديث هام بخصوص طلبك"
#         # recipient = [instance.customer_email]

#         # context = {
#         #     "name": instance.full_name_ar,
#         #     "status": instance.get_status_display(),
#         # }

#         # html_content = render_to_string("email_template.html", context)

#         # text_content = strip_tags(html_content)

#         # msg = EmailMultiAlternatives(subject, text_content, None, recipient)
#         # msg.attach_alternative(html_content, "text/html")
#         # msg.send()

#     # else :
#     #     fields_map = [
#     #         ("الحساب البنكي", "iban_status", "iban_notes"),
#     #         ("الشهادة العلمية", "degree_status", "degree_notes"),
#     #         ("عضوية المهندسين", "sce_status", "sce_notes"),
#     #         ("السيرة الذاتية", "cv_status", "cv_notes"),
#     #         ("المعدات", "equipment_status", "equipment_notes"),
#     #     ]

#     #     failed_items = []

#     #     for label, status_field, notes_field in fields_map:

#     #         status = getattr(instance, status_field)
#     #         notes = getattr(instance, notes_field)

#     #         if status == "rejected":
#     #             failed_items.append({
#     #                 'label': label,
#     #                 'notes': notes
#     #             })

#     #     if failed_items:
#     #         context = {
#     #             'name': instance.customer_name,
#     #             'failed_items': failed_items,
#     #         }

#     async_to_sync(channel_layer.group_send)(
#         f"client_{instance.account.phone}",
#         {
#             "type": "client_update",
#             "data": {
#                 "type": "applicant_status_updated",
#                 # 1
#                 "iban_notes": instance.iban_notes,
#                 "iban_status": instance.iban_status,
#                 # 2
#                 "degree_notes": instance.degree_notes,
#                 "degree_status": instance.degree_status,
#                 # 3
#                 "sce_notes": instance.sce_notes,
#                 "sce_status": instance.sce_status,
#                 # 4
#                 "cv_notes": instance.cv_notes,
#                 "cv_status": instance.cv_status,
#                 # 5
#                 "equipment_notes": instance.equipment_notes,
#                 "equipment_status": instance.equipment_status,
#                 # status
#                 "status": instance.status,
#             },
#         },
#     )


# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags


# # @receiver(post_save, sender=FieldVisit)
# # def update_engineer_live_ui(sender, instance, **kwargs):

# #     def send_data():
# #         engineer = instance.engineer
# #         wallet_obj = engineer.user.wallet
# #         channel_layer = get_channel_layer()
# #         room_group_name = f"engineer_{engineer.user.id}"
# #         new_numbers = {
# #             "total": float(wallet_obj.get_total_earnings(FieldVisit)),
# #             "frozen": float(wallet_obj.get_pending_balance(FieldVisit)),
# #             "withdrawable": float(wallet_obj.get_withdrawable_balance(FieldVisit)),
# #         }
# #         async_to_sync(channel_layer.group_send)(
# #             room_group_name, {"type": "wallet_update_event", "numbers": new_numbers}
# #         )

# #     transaction.on_commit(send_data)

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from Client.models import WalletTransaction


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver([post_save, post_delete], sender=WalletTransaction)
def wallet_transaction_changed(sender, instance, **kwargs):
    wallet = getattr(instance, 'wallet', None)
    if not wallet:
        return

    staff_profile = getattr(wallet, 'wallet', None)
    if not staff_profile or not staff_profile.user:
        return

    userID = staff_profile.user.id
    if not userID:
      return


    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{userID}",
        {
            "type": "wallet_update",
            "wallet": wallet.get_wallet_summary(),
        }
    )
