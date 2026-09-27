from Admin.models import FinancialSettings
from decimal import Decimal
from .models import PropertyPricing
from .models import Order
import requests
from django.shortcuts import render, redirect

def get_financial_settings():
    settings = FinancialSettings.objects.first()
    if not settings:
        raise ValueError("لم يتم إعداد الإعدادات المالية بعد. الرجاء إضافة سجل في الإعدادات المالية.")

    tax_rate = settings.tax_rate / 100
    company_share = settings.company_profit_percent / 100
    engineer_share = settings.engineer_profit_percent / 100
    return tax_rate, company_share, engineer_share


def calculate_inspection_price(p_type, i_type, p_size):
    try:
        service = PropertyPricing.objects.get(key=p_type)
        meter_rate = service.meter_rate or 0
        price_map = {'comprehensive': service.comp_price,'standard': service.std_price,}
        base_price = price_map.get(i_type, service.std_price)
        extra_meters = max(0, Decimal(p_size) - 200)
        return base_price + (extra_meters * meter_rate)
    except (PropertyPricing.DoesNotExist, ValueError, TypeError) as e:
        return 0


from geopy.geocoders import Nominatim
def get_address_from_coords(lat, lon):
    try:
        geolocator = Nominatim(user_agent="v_inspection_system")
        location = geolocator.reverse(f"{lat}, {lon}", language='ar')
        if location:
            address = location.raw.get('address', {})
            # city = address.get('city', address.get('town', address.get('state', '')))
            district = address.get('suburb', address.get('neighbourhood', 'حي غير معروف'))
            street = address.get('road', 'شارع غير معروف')
            return {
                #'city': city,
                'district': district,
                'street': street,
                #'full_address': location.address,
                'url':f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            }
    except Exception as e:
        print(f"Error in geopy: {e}")
    return None


from config import session_value
from Client.models import UserPhone
def get_logged_user(request):
    phone = session_value(request, key="user")
    if not phone:
        return None
    user = UserPhone.objects.filter(phone=phone).first()
    return user
