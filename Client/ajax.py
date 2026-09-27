from django.shortcuts import render

# Create your views here.


import json
from django.apps import apps
from django.shortcuts import get_object_or_404
from Client.models import Order
from Admin.models import PropertyPricing, WorkDay
from django.http import JsonResponse
# from Visits.models import Room, RoomItem


def visit_price(request):
    data = json.loads(request.body)

    type_ = data.get("type")

    try:
        size = int(data.get("size", 0))
    except (ValueError, TypeError):
        return JsonResponse({"error": "invalid size"}, status=400)

    if not type_ or not size:
        return JsonResponse({"error": "invalid data"}, status=400)

    prices = PropertyPricing.objects.filter(key=type_).first()

    if not prices:
        return JsonResponse({"error": "invalid type"}, status=400)

    free = prices.free_meters

    meter = prices.meter_rate
    normal = prices.std_price

    full = prices.comp_price
    extra = max(0, size - free)
    return JsonResponse(
        {
            "normal_price": int(normal + extra * meter),
            "full_price": int(full + extra * meter),
        }
    )


def consultation_day(request):
    work_days = WorkDay.objects.all()
    data = []
    for day in work_days:
        if day.is_working:
            data.append(
                {
                    "num": day.number,
                    "name": day.name_ar,
                    "price": int(day.total_price),
                    "start_time": str(day.start_time),
                    "end_time": str(day.end_time),
                }
            )

    return JsonResponse(data, safe=False)
