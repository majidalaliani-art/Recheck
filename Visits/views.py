# from constants import VISITS_ENGINEERKEY_PATH as PATH
from .constants import PATH
from django.core.files.storage import default_storage
import logging
logger = logging.getLogger(__name__)


from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import VisitReport,AreaImage
from Client.models import WalletTransaction


from .forms import VisitReportForm, panel_1_Form, panel_2_Form
from datetime import datetime
from Engineer.utils import check_and_compress_file
from .constants import AREA_CHOICES,INSPECTION_ITEMS,CATEGORY_CHOICES


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.db.models import Max
from django.db import models
from .utils import get_model_instance,get_model_class


from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.http import HttpResponse

from django.apps import apps
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import VisitReport,InspectionItem,ReportRecommendation,InspectionArea,AreaImage,InspectionItemImage

from django.conf import settings
from django.http import JsonResponse
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin


class VisitView(LoginRequiredMixin,View):
    template_name = PATH["VISIT"]
    def get(self, request, pk):
        Order = get_object_or_404(VisitReport, Request__visit_id=pk,Request__engineer=request.user)
        if Order.Request.status == "under_review":
            return redirect("operations:visit_review", pk=pk)
        elif Order.Request.status != "in_progress":
            return redirect("Staff:in_progress_orders")

        form = VisitReportForm(
            instance=Order,
            initial={
                "neighborhood": Order.neighborhood or Order.Request.neighborhood,
                "city": Order.Request.city,
                "requestType": Order.Request.inspection_type,
                "propertyType": Order.Request.property_type,
                "building_area_sqm": Order.building_area_sqm
                or Order.Request.property_size,
                "date": Order.date or Order.Request.day,
                "time": Order.time or datetime.now().strftime("%H:%M"),
            },
        )

        context = {
            "status":Order.Request.status,
            "form": form,
            "id": Order.Request.visit_id,
            "city": Order.Request.city.code,
            "Order": Order,
            "inspection_items":INSPECTION_ITEMS,

        }

        return render(request, self.template_name, context)
    def post(self, request, pk):
        if request.POST.get('action') == 'submit_report':
            Order = get_object_or_404(VisitReport, Request__visit_id=pk,Request__engineer=request.user)
            if Order.Request.status == "in_progress":
                Order.Request.status = "under_review"
                Order.Request.save()
                return redirect("operations:visit_review", pk=pk)



        return redirect(request.path)

class StaffVisitReviewView(LoginRequiredMixin,View):
    template_name = PATH["VISIT"]
    def get(self, request, pk):
        Order = get_object_or_404(VisitReport, Request__visit_id=pk)
        responsible = request.user

        is_staff = (Order.Request.engineer == responsible)
        is_admin = responsible.is_superuser
        if not is_staff and not is_admin:
            return redirect("Staff:under_review_orders")
        if Order.Request.status != "under_review" :
            if is_admin:
                return redirect("Admin:under_review_orders")
            else:
                return redirect("Staff:under_review_orders")


        form = VisitReportForm(
            instance=Order,
            initial={
                "neighborhood": Order.neighborhood or Order.Request.neighborhood,
                "city": Order.Request.city,
                "requestType": Order.Request.inspection_type,
                "propertyType": Order.Request.property_type,
                "building_area_sqm": Order.building_area_sqm
                or Order.Request.property_size,
                "date": Order.date or Order.Request.day,
                "time": Order.time or datetime.now().strftime("%H:%M"),
            },
        )


        context = {
            "status":Order.Request.status,
            "form": form,
            "id": Order.Request.visit_id,
            "city": Order.Request.city.code,
            "Order": Order,
            "inspection_items":INSPECTION_ITEMS,

        }

        return render(request, self.template_name, context)
















# class SupervisorVisitView(View):
#     template_name = PATH["REVIEW"]
#     def get(self, request, pk):
#         Order = get_object_or_404(VisitReport, Request__visit_id=pk)
#         url_name = request.resolver_match.url_name
#         # if url_name == "supervisor_visit_review":
#         #     if not request.user.is_superuser:
#         #         return redirect("Client:homepage")
#         #     elif Order.Request.status != "under_review" :
#         #         return redirect("Admin:under_review_orders")

#         # elif url_name == "visit":
#         #     if Order.Request.status != "completed" :
#         #         return redirect("Client:homepage")



#         unique_keys = InspectionItem.objects.filter(area__visit=Order,is_available=True).values_list('key', flat=True).distinct()




#         results = {}
#         for key in unique_keys:
#              results[key] = Order.get_overall_item_score(key)
#         print(results)




#         overall_score = Order.get_overall_property_score()






#         context = {
#             "status":Order.Request.status,
#             "visit_id": Order.Request.visit_id,
#             "Order_id": Order.Request.order.order_id,
#             "Visit": Order,

#             "results":results,
#             "overall_score":overall_score,

#         }

#         return render(request, self.template_name, context)





from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View
# weasyprint imported conditionally in ExportVisitPDFView
import base64
from io import BytesIO
import qrcode


def get_qr_code(url):
    qr_img = qrcode.make(url)
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def get_visit_context(pk):
    order = get_object_or_404(VisitReport.objects.select_related('Request__order'),Request__visit_id=pk)

    unique_keys = InspectionItem.objects.filter(area__visit=order,is_available=True).values_list('key', flat=True).distinct()

    results = {
        key: order.get_overall_item_score(key)
        for key in unique_keys
    }



    unique_categories = {}

    for area in order.areas.all():
        for item in area.items.all():
            if item.key not in unique_categories:
                unique_categories[item.key] = {
                    'key': item.key,
                    'name': item.get_key_display()
                }





    # # رقم العضوية كامل من الداتابيز
    # membership_id = visit.inspector.license_number

    # دمج الرقم في الرابط الأساسي للهيئة
    saudi_eng_url = f"https://eservices.saudieng.sa/ar/accreditation/pages/validation.aspx?Membershipid=11111111111"






    return {
        "status": order.Request.status,
        "visit_id": order.Request.visit_id,
        "Order_id": order.Request.order.order_id,
        "Visit": order,
        "qr_code_base64" : get_qr_code(saudi_eng_url),
        "inspector_verification_url":saudi_eng_url,

        "categories_list": list(unique_categories.values()),
        "images":InspectionItemImage.objects.filter(item__area__visit=order).select_related('item', 'item__area'),
        "results": results,
        "overall_score": order.get_overall_property_score(),
    }

# 1. الرابط الأول: عرض الصفحة للمستخدم
class SupervisorVisitView(View):
    template_name = PATH["REVIEW"]

    def get(self, request, pk):
        context = get_visit_context(pk)
        context["is_pdf"] = False
        return render(request, self.template_name, context)


class ExportVisitPDFView(View):
    template_name = PATH["REVIEW"]

    def get(self, request, pk):
        context = get_visit_context(pk)
        context["is_pdf"] = True

        html_string = render_to_string(
            self.template_name,
            context,
            request=request,
        )

        try:
            from weasyprint import HTML
            pdf = HTML(
                string=html_string,
                base_url=request.build_absolute_uri('/')
            ).write_pdf()
        except Exception as e:
            return HttpResponse(f"PDF generation error: {e}", status=500)

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{pk}.pdf"'
        return response






def update_status_by_supervisor(request ,Id):
    if request.method == 'POST':
        order = get_object_or_404(VisitReport.objects.select_related('Request__order'),Request__visit_id=Id)
        action = request.POST.get('action')
        if not request.user.is_superuser:
            return redirect('Client:homepage')

        elif order.Request.status != "under_review":
            return redirect('Client:homepage')


        elif action == 'reject':
            order.Request.status = "in_progress"
            order.Request.save()
            return redirect('operations:visit_review', Id)

        elif action == 'accept':
            order.Request.status = "completed"
            WalletTransaction.objects.filter(order=order.Request.order).update(status='completed')
            order.Request.save()
            return redirect('operations:visit', Id)




def save_report(request ,Id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    panel = request.POST.get("panel")
    action = request.POST.get("action")
    model_name = request.POST.get("model_name")
    table_id = request.POST.get("id")


    if not table_id or not table_id.isdigit():
        return JsonResponse({"status": "error","message": "معرّف البطاقة (ID) مطلوب، ويجب أن يكون رقماً صحيحاً."}, status=400)

    visit = get_object_or_404(VisitReport, Request__visit_id=Id, Request__engineer=request.user)
    if visit.Request.status != "in_progress":
        return JsonResponse({"status": "error","message": "عذراً، لا يمكن إجراء أي تعديل لأن حالة الزيارة الحالية لا تسمح بذلك."}, status=400)

    if model_name == "AreaImage":
        if action == "save":
            try:
                area = InspectionArea.objects.get(id=table_id)
            except InspectionArea.DoesNotExist:
                return JsonResponse({"status": "error", "message": "المنطقة المطلوبة غير موجودة"}, status=404)

            imag = request.FILES.get("images")
            if not imag:
                return JsonResponse({"status": "error", "message": "لم يتم إرفاق صورة"}, status=400)

            success, processed_file = check_and_compress_file(imag, file="image")
            if success:
                try:
                    obj = AreaImage.objects.create(area=area, image=processed_file)
                    return JsonResponse({"status": "success","id": obj.id,"url": obj.image.url})
                except Exception as e:
                    logger.error(f"Failed to upload general image to cloud: {e}")
                    return JsonResponse({"status": "error", "message": "فشل ضغط الصورة"}, status=500)
            else:
                return JsonResponse({"status": "error", "message": "فشل ضغط الصورة"}, status=400)


        elif action == "delete":
            try:
                table = AreaImage.objects.get(id=table_id)
                if table.image:
                    table.image.delete(save=False)
                table.delete()
                return JsonResponse({"status": "success"}, status=200)
            except InspectionItemImage.DoesNotExist:
                return JsonResponse({"status": "error", "message": "السجل غير موجود"}, status=404)
            except Exception as e:
                logger.error(f"Failed to delete general image with ID {table_id}: {e}")
                return JsonResponse({"status": "error","message": "فشل حذف الصورة العامة"},status=500)
        else:
            return JsonResponse({"status": "error","message": "القيمه ليست صحيحه في action"},status=400)




    elif model_name == "InspectionItemImage":
        if action == "save":
            comment = request.POST.get("comment")
            image = request.FILES.get("image")
            if not image or not comment or not comment.strip():
                return JsonResponse({"status": "error","message": "جميع البيانات مطلوبة (الصورة والتعليق)." }, status=400)
            success, processed_file = check_and_compress_file(image, file="image")
            if not success:
                return JsonResponse({"status": "error","error_type": "image","message": "فشل معالجة أو ضغط الصورة."})

            try:
                item = InspectionItem.objects.get(id=table_id)
                table = InspectionItemImage.objects.create(item=item,image=processed_file,comment=comment)
                return JsonResponse({"status": "success","id": table.id ,"key":table.item.key}, status=201)

            except InspectionItem.DoesNotExist:
                return JsonResponse({"status": "error", "message": "العنصر المطلوب غير موجود."}, status=404)

        elif action == "update":
            comment = request.POST.get("comment")
            if not comment or not comment.strip():
                return JsonResponse({"status": "error","message": "نص التعليق مطلوب ولا يمكن أن يكون فارغاً." }, status=400)
            try:
                table = InspectionItemImage.objects.get(id=table_id)
                clean_comment = comment.strip()
                if table.comment != clean_comment:
                    table.comment = clean_comment
                    table.save(update_fields=["comment"])
                return JsonResponse({"status": "success", "message": "تم التعديل بنجاح"}, status=200)

            except InspectionItemImage.DoesNotExist:
                return JsonResponse({"status": "error", "message": "السجل غير موجود"}, status=404)

        elif action == "delete":
            try:
                table = InspectionItemImage.objects.get(id=table_id)
                if table.image:
                    table.image.delete(save=False)
                table.delete()
                return JsonResponse({"status": "success", "message": "تم الحذف بنجاح"}, status=200)
            except InspectionItemImage.DoesNotExist:
                return JsonResponse({"status": "error", "message": "السجل غير موجود"}, status=404)
            except Exception as e:
                logger.error(f"Delete failed for ID {table_id}: {e}")
                return JsonResponse({"status": "error", "message": "فشل الحذف، حدث خطأ في السحابة"}, status=500)
        else:
            return JsonResponse({"status": "error","message": "القيمه ليست صحيحه في action"},status=400)




    elif model_name == "VisitReport":
        visit = get_model_instance("Visits","VisitReport",table_id)
        if visit is None :
            return JsonResponse({"status": "error", "message": "المنطقة غير موجودة"},status=400)

        if panel == "1":
            if "property_image" in request.FILES:
                raw_file = request.FILES["property_image"]
                print(raw_file)
                success, processed_file = check_and_compress_file(raw_file, file="image")
                if success:
                    request.FILES["property_image"] = processed_file
                else:
                    del request.FILES["property_image"]
            form = panel_1_Form(request.POST, request.FILES, instance=visit)
        elif panel == "2":
            form = panel_2_Form(request.POST,instance=visit)
        else:
            return JsonResponse({"status": "error", "message": "رقم البانل غير موجود"}, status=400)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success", "message": "تم حفظ التقرير بنجاح"})
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)

    else:
        return JsonResponse({"status": "error", "message": "قيمة غير متطابقة"}, status=400)








def save_inspection_items(request,Id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            if not isinstance(data, dict):
                return JsonResponse({"error": "بنية البيانات غير صحيحة"}, status=400)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({"error": "بيانات JSON غير صالحة"}, status=400)
        visit = get_object_or_404(VisitReport, Request__visit_id=Id, Request__engineer=request.user)
        if visit.Request.status != "in_progress":
            return JsonResponse({"status": "error","message": "عذراً، لا يمكن إجراء أي تعديل لأن حالة الزيارة الحالية لا تسمح بذلك."}, status=400)


        table_id = data.get("id")
        action = data.get("action")
        model_name = data.get("name")


        if model_name == 'InspectionArea':
            items = data.get("items")




            if action == "add":
                instance = get_model_instance("Visits","VisitReport",table_id)
                if instance is None :
                    return JsonResponse({"status": "error", "message": "المنطقة غير موجودة"},status=400)
                elif not items:
                    return JsonResponse({"error": "لا توجد بيانات للحفظ"}, status=400)

                key = instance.Request.inspection_type.key
                if key == "standard":


                    if items != "general":
                        return JsonResponse(
                            {"status": "failed","message": "نوع المنطقة غير صحيح"},status=400)
                    try:
                        new_area, created = InspectionArea.objects.get_or_create(visit=instance,key="general",)

                        if created:
                            return JsonResponse({
                                "status": "success",
                                "id": new_area.id,
                                "address": new_area.get_key_display(),
                                "created": True,
                            })

                        return JsonResponse({
                            "status": "exists",
                            "id": new_area.id,
                            "address": new_area.get_key_display(),
                            "message": "الكرت العام موجود مسبقاً",
                        })

                    except Exception as e:
                        return JsonResponse(
                            {"status": "failed","message": "حدث خطأ أثناء إنشاء الكرت العام",},status=500)

                elif key == "complete":
                    if items == "general" :
                        return JsonResponse({"status": "failed"})
                    elif items not in list(dict(AREA_CHOICES).keys()):
                        return JsonResponse({"status": "failed"})

                    try:
                        new_area = InspectionArea.objects.create(visit=instance, key=items)
                        return JsonResponse({"status": "success", "id": new_area.id  ,"address":new_area.get_key_display()})
                    except Exception as e:
                        return JsonResponse({"status": "failed"})

                else:
                    return JsonResponse({"status": "error", "message": "قيمة غير متطابقة"}, status=400)


            elif action == "update_title":
                instance = get_model_instance("Visits", "InspectionArea", table_id)
                if instance is None:
                    return JsonResponse({"status": "error", "message": "المنطقة غير موجودة"},status=400)
                elif not items:
                    return JsonResponse({"error": "لا توجد بيانات للحفظ"}, status=400)

                if instance.name != items:
                    instance.name = items
                    instance.save(update_fields=["name"])

                return JsonResponse({"status": "success"})

            elif action == "Delete the motherboard":
                instance = get_model_instance("Visits", "InspectionArea", table_id)
                if instance is None:
                    return JsonResponse({"status": "error", "message": "المنطقة غير موجودة"},status=400)

                try:
                    if hasattr(default_storage, "bucket"):
                        default_storage.bucket.objects.filter(Prefix=instance.folder_path).delete()
                    instance.delete()

                    return JsonResponse({"status": "success"})

                except Exception as e:
                    logger.error(f"Delete failed for ID {table_id}: {e}")
                    return JsonResponse(
                        {"status": "error","message": "فشل الحذف، حدث خطأ أثناء حذف الملفات أو السجل"},status=500)


            elif action == 'create':
                instance = get_model_instance("Visits", "InspectionArea", table_id)
                if instance is None:
                    return JsonResponse({"status": "error", "message": "المنطقة غير موجودة"},status=400)
                elif not items:
                    return JsonResponse({"error": "لا توجد بيانات للحفظ"}, status=400)

                created_items = []
                for item in items:
                    if item not in list(dict(CATEGORY_CHOICES).keys()):
                        continue
                    elif not InspectionItem.objects.filter(area=instance, key=item).exists():
                        new_item = InspectionItem.objects.create(area=instance, key=item)
                        created_items.append({
                            "id": new_item.id,
                            "key": new_item.key,
                            "name": new_item.get_key_display(),
                            "available":new_item.is_available,
                            # "score":new_item.score,
                        })


                    else:
                        continue
                return JsonResponse({"status": "success", "created_items": created_items})

            elif action == 'delete':
                try:
                    item = InspectionItem.objects.get(id=table_id)
                    if hasattr(default_storage, 'bucket'):
                        default_storage.bucket.objects.filter(Prefix=item.folder_path).delete()
                    item.delete()
                    return JsonResponse({"status": "success"})
                except InspectionItem.DoesNotExist:
                    return JsonResponse({"status": "error"}, status=404)
                except Exception as e:
                    logger.error(f"Delete failed for ID {table_id}: {e}")
                    return JsonResponse({"status": "error", "message": "فشل الحذف، حدث خطأ في السحابة"}, status=500)




            elif action == 'update':
                ModelClass=get_model_class('Visits','InspectionItem')
                if not ModelClass:
                    return JsonResponse({"status": "error", "message": "الجدول غير موجود"},status=400)
                elif not items:
                    return JsonResponse({"error": "لا توجد بيانات للحفظ"}, status=400)
                for item in items:
                    item_id = item.get('id')
                    is_available = item.get('is_available')
                    score = item.get('score')
                    if not item_id or not item_id.isdigit():
                        return JsonResponse({"status": "error","message": "معرّف البطاقة (ID) مطلوب، ويجب أن يكون رقماً صحيحاً."}, status=400)


                    if is_available is True or is_available is False:

                        try:
                            score = int(score)
                        except (TypeError, ValueError):
                            continue

                        if score < 0:
                            continue
                        try:
                            instance = ModelClass.objects.get(id=item_id)
                            if instance.is_available != is_available or instance.score != score:
                                instance.is_available = is_available
                                instance.score = score
                                instance.save()
                        except ModelClass.DoesNotExist:
                            continue
                    else:
                        continue

                return JsonResponse({'status': 'success',})



            else:
                return JsonResponse({"status": "error", "message": "قيمة غير متطابقة"}, status=400)


        if model_name == 'ReportRecommendation':


            if action == "save":
                instance = get_model_instance("Visits", "VisitReport", table_id)
                if instance is None:
                    return JsonResponse({"status": "error", "message": "الزيارة غير موجودة"}, status=400)
                max_number = ReportRecommendation.objects.filter(visit=instance).aggregate(Max('number'))['number__max']
                next_number = (max_number + 1) if max_number is not None else 1
                try:
                    rec = ReportRecommendation.objects.create(visit=instance, number=next_number)
                    return JsonResponse({"status": "success","id":rec.id,"number":rec.number,"message": "تمت الإضافة بنجاح"})
                except IntegrityError:
                    return JsonResponse({"error": "نص التوصية مكرر لهذه الزيارة"}, status=400)

            elif action == "delete":
                try:
                    instance = get_model_instance("Visits", "ReportRecommendation", table_id)
                    if instance is None:
                        return JsonResponse({"status": "error", "message": "التوصية غير موجودة"}, status=400)
                    visit_instance = instance.visit
                    deleted_number = instance.number
                    instance.delete()
                    ReportRecommendation.objects.filter(visit=visit_instance,number__gt=deleted_number).update(number=models.F("number") - 1)
                    return JsonResponse({"status": "success", "message": "تم حذف التوصية بنجاح"})
                except Exception as e:
                    return JsonResponse({
                        "status": "error","message": "حدث خطأ في الاتصال أو قاعدة البيانات، يجدر المحاولة لاحقاً" }, status=500)

            elif action == "update":
                text = data.get("text")
                instance = get_model_instance("Visits", "ReportRecommendation", table_id)
                if instance is None:
                    return JsonResponse({"status": "error", "message": "التوصية غير موجودة"}, status=400)
                elif not text or not text.strip():
                    return JsonResponse({"error": "لا توجد بيانات للحفظ"}, status=400)

                text = text.strip()
                if instance.text != text:
                    instance.text = text
                    instance.save()

                return JsonResponse({"status": "success","message": "تم الحفظ بنجاح"})



            else:
                return JsonResponse({"status": "error", "message": "قيمة غير متطابقة"}, status=404)




    return JsonResponse({"error": "Method not allowed"}, status=405)





def visit_inspection_view(request, table_id):

    INSPECTION_FIELDS_FIRST=[
        "property_image",
        "date",
        "time",
        "neighborhood",
        "unit_number",
        "detailed_address",
        "latitude",
        "longitude",
    ]


    INSPECTION_FIELDS_SECOND = [
        # "property_owner",
        "number_of_floors",
        # "building_license_number",
        # "property_developer",
        # "design_office",
        # "engineering_supervisor",
        # "electricity_meter_reading",
        # "water_meter_reading",
        "property_age_years",
        "building_area_sqm",
        # "electricity_meter_number",
        # "water_meter_number",
    ]

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


    instance = get_model_instance("Visits", "VisitReport", table_id)
    if instance is None:
        return JsonResponse({"status": "error", "message": "الزيارة غير موجودة"}, status=400)

    elif instance.Request.engineer != request.user:
        return JsonResponse({"status": "error", "message": "مستخدم غير صحيح"}, status=404)
    elif instance.Request.status != "in_progress":
        return JsonResponse({"status": "error","message": "عذراً، لا يمكن إجراء أي تعديل لأن حالة الزيارة الحالية لا تسمح بذلك."}, status=400)


    missing_fields = []

    pages_to_check = [
        (1, INSPECTION_FIELDS_FIRST),
        (2, INSPECTION_FIELDS_SECOND),
    ]

    for page_num, fields_list in pages_to_check:
        if page_num == 1:
            for field_name in fields_list:

                value = getattr(instance, field_name, None)
                if field_name == "property_image" and not value:
                    missing_fields.append({"message": "لا يوجد صورة في ( بيانات العقار ) لم يتم إدخالها بشكل صحيح أو لم يتم حفظها."})



                elif value is None or (isinstance(value, str) and value.strip() == ""):
                    missing_fields.append({"message": "بعض ( بيانات العقار ) المطلوبة لم يتم إدخالها بشكل صحيح أو لم يتم حفظها."})
                    break


        elif page_num == 2:
            for field_name in fields_list:
                value = getattr(instance, field_name, None)
                if value is None or (isinstance(value, str) and value.strip() == ""):
                    missing_fields.append({"message": "بعض ( مواصفات ومستندات العقار ) المطلوبة لم يتم إدخالها بشكل صحيح أو لم يتم حفظها."})
                    break




    has_areas = instance.areas.exists()
    if not has_areas:
        missing_fields.append({"message": "يلزم إضافة مساحة في قسم (ملاحظات الفحص) قبل حفظ التقرير."})
    for area in instance.areas.all():
        has_items = area.items.exists()
        area_display_name = area.name.strip() if (area.name and area.name.strip()) else area.get_key_display()
        general_image = area.images.exists()
        if not general_image:
            missing_fields.append({"message": f"لا توجد أي صور عامة في ({area_display_name})."})

        if not has_items:
            missing_fields.append({"message": f"توجد بنود غير مكتملة في ({area_display_name}) بقسم (ملاحظات الفحص)."})
        for item in area.items.all():
            item_images = item.images.all()
            item_display_name = item.get_key_display()
            if not item_images.exists():
                missing_fields.append({"message": f"يلزم إضافة صورة واحدة على الأقل لبند ({item_display_name}) في ({area_display_name})."})

    has_recommendations = instance.recommendations.exists()
    if not has_recommendations:
        missing_fields.append({"message": "يلزم إضافة توصية واحدة على الأقل في قسم ( التوصيات النهائية ) قبل حفظ التقرير." })
    else:
        for rec in instance.recommendations.all():
            if not rec.text or not rec.text.strip():
                missing_fields.append({
                "message": "توجد توصية فارغة في قسم (التوصيات النهائية)، يلزم كتابة نص التوصية أو حذفها."
                })
                break






    if missing_fields:
        return JsonResponse({
            "status": "error",
            "message": "يوجد حقول مطلوبة لم يتم تعبئتها",
            "items": missing_fields
        })

    return JsonResponse({
        "status": "success",
        "message": "جميع الحقول مكتملة ولا توجد مشاكل"
    })
