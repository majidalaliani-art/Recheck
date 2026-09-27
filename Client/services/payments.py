from django.conf import settings
import stripe
from django.urls import reverse
stripe.api_key = settings.PAYMENT_SECRET_KEY

def create_checkout_session(order):
    # success_url = reverse("order_success", args=[order.order_id])

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"Order {order.order_id}",
                    },
                    "unit_amount": int(order.payment.amount * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/success/",
        cancel_url="http://127.0.0.1:8000/cancel/",
    )

    return session




def create_payment_intent(order):
    intent = stripe.PaymentIntent.create(
        amount=int(order.payment.amount * 100),
        currency="usd",
        metadata={"order_id": order.order_id},
        automatic_payment_methods={"enabled": True},
    )

    return intent
