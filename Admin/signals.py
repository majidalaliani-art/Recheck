

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Region

@receiver(post_save, sender=Region)
def create_group_for_region(sender, instance, created, **kwargs):
    if created:
        Group.objects.get_or_create(name=instance.code)

@receiver(pre_delete, sender=Region)
def delete_group_for_region(sender, instance, **kwargs):
    Group.objects.filter(name=instance.code).delete()
