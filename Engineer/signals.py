from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from Client.models import WalletTransaction


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
