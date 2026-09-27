from ..models import Order, Payment
from Admin.models import FinancialSettings,Coupon


def create_order(user, type_service, price):
    order = Order.objects.create(client=user, order_type=type_service)
    Payment.objects.create(order=order, amount=price, status="pending")
    return order

    # if coupon:
    #     coupon_obj = Coupon.objects.filter(code=coupon, is_active=True).first()
    #     if coupon_obj:
    #         final_price = price - (price * coupon_obj.discount_percent / 100)
    #         coupon_obj.delete()
