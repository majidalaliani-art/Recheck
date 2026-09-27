
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from Client.models import Order
from Visits.models import FieldVisit
from decimal import Decimal

from Admin.models import GlobalSettings

class Command(BaseCommand):
    print(11)


    def handle(self, *args, **options):
        cutoff_time = timezone.now() - timedelta(minutes=1)
        print(11)
        orders = Order.objects.filter(
            created_at__lte=cutoff_time,

            processed=False
        )
        tax_settings = GlobalSettings.objects.filter(settings_type='tax').first()
        if tax_settings:
            tax_rate = tax_settings.tax_rate / 100
            p_percent = tax_settings.company_profit_percent
            e_percent = tax_settings.engineer_profit_percent
        else:
            # قيم افتراضية إذا لم توجد إعدادات
            tax_rate = Decimal('0.15')
            p_percent = 20
            e_percent = 80

        for order in orders:
            price = order.final_price
            tax = price * tax_rate
            p_amount = tax * (p_percent / 100)
            e_amount = tax * (e_percent / 100)
            print(p_percent)


        # count = 0
        # for order in orders:

        #     price = order.final_price
        #     tax_rate = Decimal('0.15')
        #     p_amount = tax_rate * Decimal('0.20')
        #     e_amount = tax_rate *  Decimal('0.80')

        #     # إنشاء زيارة ميدانية مرتبطة بالطلب
        #     FieldVisit.objects.create(
        #         order=order,
        #         # أي حقول أخرى تحتاجها
        #     )

        #     # تحديث حالة الطلب
        #     order.processed = True
        #     order.save()
        #     count += 1

        self.stdout.write(self.style.SUCCESS(f'تم إنشاء {count} زيارة ميدانية'))
