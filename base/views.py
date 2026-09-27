# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from .constants import PATH
import json
from django.apps import apps
from django.shortcuts import get_object_or_404
from Client.models import Order
from .utils import process_and_replace_image, is_file_duplicate
from Admin.models import PropertyPricing, WorkDay
from django.http import JsonResponse
# from Visits.models import Room, RoomItem
from django.contrib.auth import logout


def upload_single_file(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        Id = request.POST.get("id")
        table = request.POST.get("table")
        type = request.POST.get("type")
        category = request.POST.get("category")
        if not file or not Id or not table or not type or not category:
            return JsonResponse(
                {"status": "error", "message": "No file provided"}, status=400
            )
        if table.lower() == "order":
            obj = Order.objects.filter(order_id=Id).first()
            if category.lower() == "image":
                if type.lower() == "entrance_image":
                    if process_and_replace_image(obj, "entrance_image", file):
                        return JsonResponse(
                            {
                                "status": "success",
                                "message": "File uploaded successfully",
                            },
                            status=200,
                        )
                    else:
                        return JsonResponse(
                            {"status": "error", "message": "Failed to process file"},
                            status=400,
                        )
                else:
                    return JsonResponse(
                        {"status": "error", "message": "Invalid type"}, status=400
                    )
            else:
                return JsonResponse(
                    {"status": "error", "message": "Invalid category"}, status=400
                )

        else:
            return JsonResponse(
                {"status": "error", "message": "Invalid table"}, status=400
            )
    return JsonResponse({"status": "error", "message": "Invalid table"}, status=400)


# TABLE_MODELS = {
#     "room": Room,
#     "order": Order,
# }


# def create_card(request):
#     if request.method == "POST":
#         Id = request.POST.get("id")
#         table = request.POST.get("table").lower()
#         action = request.POST.get("action").lower()
#         name = request.POST.get("name")

#         if not Id or not table or not action:
#             return JsonResponse(
#                 {"status": "error", "message": "Missing required fields"}, status=400
#             )

#         if table == "room" and action == "add" and name:
#             try:
#                 visit = FieldVisit.objects.select_related("order").get(pk=Id)
#                 inspection_type = visit.order.inspection_type
#                 if inspection_type == "comprehensive":

#                     room = Room.objects.create(visit=visit, name=name)
#                     return JsonResponse(
#                         {"status": "success", "id": room.pk, "name": room.name},
#                         status=200,
#                     )
#                 else:
#                     return JsonResponse(
#                         {"status": "success", "message": "No room can be added"},
#                         status=403,
#                     )

#             except FieldVisit.DoesNotExist:

#                 return JsonResponse(
#                     {"status": "error", "message": "Visit not found"}, status=404
#                 )

#         if table == "roomitems" and action == "add" and name:
#             try:
#                 room = Room.objects.get(pk=Id)

#                 roomitem = RoomItem.objects.create(room=room, name="name")
#                 return JsonResponse(
#                     {"status": "success", "id": roomitem.pk, "name": roomitem.name},
#                     status=200,
#                 )
#             except Room.DoesNotExist:
#                 return JsonResponse(
#                     {"status": "error", "message": "Room not found"}, status=404
#                 )

#         if table in TABLE_MODELS and action == "delete":
#             table_model = TABLE_MODELS.get(table)
#             if not table_model:
#                 return JsonResponse(
#                     {"status": "error", "message": "Invalid table"}, status=400
#                 )
#             try:
#                 obj = table_model.objects.get(pk=Id)
#                 obj.delete()
#                 return JsonResponse({"status": "success"}, status=200)
#             except table_model.DoesNotExist:
#                 return JsonResponse(
#                     {"status": "error", "message": f"{table} not found"}, status=404
#                 )

#     return JsonResponse(
#         {"status": "error", "message": "Error in transmission"}, status=400
#     )



from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

class MyLoginView(UserPassesTestMixin, LoginView):
    template_name = PATH["LOGIN"]

    def test_func(self):
        return not self.request.user.is_authenticated


    def handle_no_permission(self):
        user = self.request.user
        referer = self.request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        if user.is_superuser or user.is_staff:
            return redirect(reverse_lazy('Admin:dashboard'))
        return redirect(reverse_lazy('Staff:available_orders'))


    def get_success_url(self):
        user = self.request.user
        redirect_to = self.request.POST.get(self.redirect_field_name, self.request.GET.get(self.redirect_field_name))
        if redirect_to:
            return redirect_to
        elif user.is_superuser or user.is_staff:
             return reverse_lazy('Admin:dashboard')
        else:
            return reverse_lazy('Staff:available_orders')


def logout_view(request):
    logout(request)
    app = request.GET.get("app")
    next_page = request.GET.get("next")
    if next_page and app:
        next_page = next_page.strip("/")
        page = app + ":" + next_page
        return redirect(page)
    return redirect("/")
