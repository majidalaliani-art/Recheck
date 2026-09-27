# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from Client.models import Order
# from django.utils import timezone
# from .models import PropertyInfo
# from Admin.models import PropertyPricing
# #from Client.utils import get_financial_settings
# from django.contrib.auth.models import Group

# @receiver(post_save, sender=FieldVisit)
# def sync_status_to_order(sender, instance, **kwargs):
#     if instance.is_null:
#         sender.objects.filter(pk=instance.pk).update(
#             engineer=None,
#             status = 'null',
#             accepted_at = None,
#             deadline = None,
#             processed = False,
#         )
#         # PropertyInfo.objects.filter(field_visit=instance.visit_id).delete()
#         instance.order.__class__.objects.filter(pk=instance.order.pk).update(status='null',)
#     elif instance.engineer:
#         if instance.processed:
#             sender.objects.filter(pk=instance.pk).update(status = 'approved',)
#             instance.order.__class__.objects.filter(pk=instance.order.pk).update(status='approved',)
#         else:
#             pricing = PropertyPricing.objects.filter(key=instance.order.property_type.key).first().allowed_duration
#             sender.objects.filter(pk=instance.pk).update(
#                 status = 'in_progress',
#                 accepted_at = timezone.now(),
#                 deadline = timezone.now() +  pricing,
#             )
#             instance.order.__class__.objects.filter(pk=instance.order.pk).update(status='in_progress',)
#     elif instance.processed:
#         sender.objects.filter(pk=instance.pk).update(
#             status = 'null',
#             processed = False
#         )
#         instance.order.__class__.objects.filter(pk=instance.order.pk).update(
#             status='null',
#         )
#     elif instance.order.status != instance.status:
#         instance.order.status = instance.status
#         instance.order.save()
