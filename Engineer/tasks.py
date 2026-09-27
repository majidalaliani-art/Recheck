from celery import shared_task
from django.utils import timezone
import logging

# إعداد السجلات
logger = logging.getLogger(__name__)


from celery import shared_task
from django.utils import timezone
from django.apps import apps
import logging

logger = logging.getLogger(__name__)


from celery import shared_task
from django.utils import timezone
from django.apps import apps
import logging

logger = logging.getLogger(__name__)


from celery import shared_task
from django.utils import timezone
from django.apps import apps
import logging

# استيراد أدوات Channels
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)


from django.apps import apps
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import logging
from Client.models import VisitDetails, ConsultationDetails,WalletTransaction
from django.utils import timezone
from Visits.models import VisitReport

from django.core.files.storage import default_storage

# @shared_task
# def send_wallet_update_task(app_label, model_name, object_id):
#     logger = logging.getLogger(__name__)

#     try:
#         Model = apps.get_model(app_label, model_name)
#         instance = Model.objects.get(pk=object_id)
#         print(instance)
#         if instance.paid_at:
#             return

#         Model.objects.filter(pk=object_id).update(
#             paid_at=timezone.now(),
#             current_task_id=None
#         )

#         instance.refresh_from_db()
#         engineer = instance.engineer
#         wallet_obj = engineer.wallet_profile
#         new_numbers = {
#             "total": float(wallet_obj.get_total_earnings(Model)),
#             "frozen": float(wallet_obj.get_pending_balance(Model)),
#             "withdrawable": float(wallet_obj.get_withdrawable_balance(Model)),
#         }

#         channel_layer = get_channel_layer()
#         room_group_name = f"engineer_{engineer.pk}"

#         async_to_sync(channel_layer.group_send)(
#             room_group_name,
#             {
#                 "type": "wallet_update_event",
#                 "numbers": new_numbers,
#             },
#         )

#     except Exception as e:
#         print(False)
#         logger.error(f"Task Error for {model_name}: {str(e)}")

@shared_task
def expire_order(ID, order):
    if order == "visit":
        visit = VisitDetails.objects.filter(visit_id=ID,status='in_progress').first()

        if not visit:
            return
        transaction = WalletTransaction.objects.filter(order=visit.order,status="pending").last()

        if transaction and visit.end_at <= timezone.now():
            instance = VisitReport.objects.filter(Request=visit).first()
            if instance:
                if hasattr(default_storage, "bucket"):
                    default_storage.bucket.objects.filter(Prefix=instance.folder_path).delete()
                instance.delete()

            visit.engineer = None
            visit.status = "published"
            visit.start_at = None
            visit.end_at = None
            visit.save()

            transaction.status = "cancel"
            transaction.cancelled_at = timezone.now()
            transaction.save()


    elif order == "Consultation":
        Consultation = ConsultationDetails.objects.filter(Consultation_id=ID).first()
        if Consultation and Consultation.status == "in_progress" and Consultation.end_at <= timezone.now():
            Consultation.engineer = None
            Consultation.status = "published"
            Consultation.start_at = None
            Consultation.end_at = None
            Consultation.save()
