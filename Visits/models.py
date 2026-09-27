from django.db import models
# from django.contrib.auth.models import User, Group
# from Client.models import Order
# import datetime, random,string
# # Create your models here.

from constants import INSPECTION_CHOICES,STATUS_DICT

# from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator


# # Import the dictionary and choices from your new file
from .constants import *

# # from Engineer.models import Engineer
# from Admin.models import PropertyPricing
from django.core.validators import MaxValueValidator, MinValueValidator
from Client.models import VisitDetails, ConsultationDetails, WalletTransaction, Payment
import os
import shutil
from django.conf import settings

# def image_ajax(instance, filename):
#     u_id = instance.field_visit.engineer.data.public_id
#     visit_id = instance.field_visit.visit_id

#     if hasattr(instance, 'property_image'):
#         sub_folder = 'property'
#     elif hasattr(instance, 'report_file'):
#         sub_folder = 'reports'
#     elif hasattr(instance, 'unit_image'):
#         sub_folder = 'unit'
#     else:
#         sub_folder = 'general'
#     return f'Visits/{u_id}/{visit_id}/{sub_folder}/{filename}'


# # ==========================================================
# # 1. PROPERTY INFORMATION MODEL (First Child)
# # Stores general details about the property, filled once per visit.
# # ==========================================================


class DynamicPathUploader:

    def __init__(self, file):
        self.file = file

    def __call__(self, instance, filename):
        Id = str(instance.Request.visit_id)

        folder_path = os.path.join(settings.MEDIA_ROOT, "Visit", Id, self.file)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        return os.path.join("Visit", Id, self.file, filename)

    def deconstruct(self):
        return (
            f"{self.__module__}.{self.__class__.__name__}",
            [self.file],
            {},
        )



from django.db import models
from django.db.models import Avg


class VisitReport(models.Model):
    Request = models.OneToOneField(
        VisitDetails,
        on_delete=models.CASCADE,
        related_name="property_info",
        verbose_name=PROPERTY_LABELS["related_visit"],
    )

    # ---------------------------------------------------
    # Text and Numeric Fields
    # ---------------------------------------------------

    neighborhood = models.CharField(max_length=100, null=True, blank=True, verbose_name=PROPERTY_LABELS['neighborhood'])
    detailed_address = models.CharField(max_length=500, null=True, blank=True, verbose_name=PROPERTY_LABELS['detailed_address'])
    latitude = models.CharField(max_length=50, null=True, blank=True, verbose_name=PROPERTY_LABELS['latitude'])
    longitude = models.CharField(max_length=50, null=True, blank=True, verbose_name=PROPERTY_LABELS['longitude'])

    unit_number = models.CharField(null=True, blank=True,max_length=10, verbose_name=PROPERTY_LABELS['unit_number'])

    date = models.DateField(null=True, blank=True, verbose_name=PROPERTY_LABELS['date'])
    time = models.TimeField(null=True, blank=True, verbose_name=PROPERTY_LABELS['time'])

    property_image = models.ImageField(
    upload_to=DynamicPathUploader(file="property_image"),null=True,blank=True,verbose_name=PROPERTY_LABELS['property_image'])

    building_activity = models.CharField(max_length=50,choices=ACTIVITY_CHOICES,default="raw",verbose_name=PROPERTY_LABELS["building_activity"],)
    property_condition = models.CharField(max_length=50,choices=CONDITION_CHOICES,default="unfurnished",verbose_name=PROPERTY_LABELS["property_condition"],)

    property_owner = models.CharField(max_length=200, null=True, blank=True, verbose_name=PROPERTY_LABELS['property_owner'])
    number_of_floors = models.PositiveIntegerField(null=True, blank=True, verbose_name=PROPERTY_LABELS['number_of_floors'])

    building_license_number = models.CharField(max_length=100, blank=True, verbose_name=PROPERTY_LABELS['building_license_number'])
    property_developer = models.CharField(max_length=200, blank=True, verbose_name=PROPERTY_LABELS['property_developer'])
    design_office = models.CharField(max_length=200, blank=True, verbose_name=PROPERTY_LABELS['design_office'])
    engineering_supervisor = models.CharField(max_length=200, blank=True, verbose_name=PROPERTY_LABELS['engineering_supervisor'])

    electricity_meter_number = models.CharField(max_length=100, blank=True, verbose_name=PROPERTY_LABELS['electricity_meter_number'])
    electricity_meter_reading = models.CharField(max_length=100, blank=True, verbose_name=PROPERTY_LABELS['electricity_meter_reading'])
    water_meter_number = models.CharField(max_length=100, blank=True, verbose_name=PROPERTY_LABELS['water_meter_number'])
    water_meter_reading = models.CharField(max_length=100, blank=True, verbose_name=PROPERTY_LABELS['water_meter_reading'])

    property_age_years = models.PositiveIntegerField(null=True, blank=True, verbose_name=PROPERTY_LABELS['property_age_years'])

    building_area_sqm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=PROPERTY_LABELS['building_area_sqm'])

    # ---------------------------------------------------
    # Boolean Fields (Neighbors)
    # ---------------------------------------------------
    street_north = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['street_north'])
    street_south = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['street_south'])
    street_east = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['street_east'])
    street_west = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['street_west'])

    building_north = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['building_north'])
    building_south = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['building_south'])
    building_east = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['building_east'])
    building_west = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['building_west'])

    # ---------------------------------------------------
    # Boolean Fields (Infrastructure)
    # ---------------------------------------------------
    infra_electricity = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['infra_electricity'])
    infra_water = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['infra_water'])
    infra_sewage = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['infra_sewage'])
    infra_asphalt = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['infra_asphalt'])
    infra_lighting = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['infra_lighting'])
    infra_network = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['infra_network'])

    # ---------------------------------------------------
    # Boolean Fields (Features)
    # ---------------------------------------------------
    feat_disabled_friendly = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['feat_disabled_friendly'])
    feat_fire_system = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['feat_fire_system'])
    feat_garden = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['feat_garden'])
    feat_parking = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['feat_parking'])
    feat_skylight = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['feat_skylight'])
    feat_pool = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['feat_pool'])
    feat_elevator = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['feat_elevator'])
    feat_cameras = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['feat_cameras'])
    feat_central_ac = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['feat_central_ac'])
    feat_water_tanks = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['feat_water_tanks'])
    feat_outdoor_seating = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['feat_outdoor_seating'])

    # ---------------------------------------------------
    # Boolean Fields (Documents)
    # ---------------------------------------------------
    doc_building_license = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['doc_building_license'])
    doc_soil_test = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['doc_soil_test'])
    doc_structural_warranty = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['doc_structural_warranty'])
    doc_architectural_plans = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['doc_architectural_plans'])
    doc_structural_plans = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['doc_structural_plans'])
    doc_electrical_plans = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['doc_electrical_plans'])
    doc_mechanical_plans = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['doc_mechanical_plans'])
    doc_survey_form = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['doc_survey_form'])
    doc_eng_supervision = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['doc_eng_supervision'])
    doc_finishes_warranty = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['doc_finishes_warranty'])
    doc_rebar_report = models.BooleanField(default=False, verbose_name=PROPERTY_LABELS['doc_rebar_report'])
    # ---------------------------------------------------


    def get_overall_item_score(self, item_key):
        result = InspectionItem.objects.filter(
            area__visit=self,
            key=item_key,
            is_available=True
        ).aggregate(
            average_score=Avg('score')
        )

        score = result["average_score"] or 0

        return {
            "name": dict(CATEGORY_CHOICES)[item_key],
            "score": score,
            "width": f"{score:.2f}".replace(",", "."),
        }
    def get_overall_property_score(self):
        result = InspectionItem.objects.filter(
            area__visit=self,
            is_available=True
        ).aggregate(overall_avg=Avg('score'))

        return result['overall_avg'] or 0


    @property
    def folder_path(self):
        visit_id = str(self.Request.visit_id)
        return f"Visit/{visit_id}/"


# (ReportRecommendation)


class ReportRecommendation(models.Model):
  visit = models.ForeignKey(VisitReport,on_delete=models.CASCADE,related_name="recommendations",)
  number = models.PositiveIntegerField(default=1,blank=True,validators=[MinValueValidator(1)],)
  text = models.TextField(verbose_name="نص التوصية", blank=True, null=True)

  class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=["visit", "text"],
            condition=models.Q(text__isnull=False) & ~models.Q(text=""),
            name="unique_non_empty_text_per_visit",),
    ]




def general_report_image_upload_path(instance, filename):
    return os.path.join(f"{instance.area.folder_path}/general_report_images/", filename)


class InspectionArea(models.Model):
    visit = models.ForeignKey(VisitReport,on_delete=models.CASCADE,related_name="areas", )
    key = models.CharField( max_length=25,choices=AREA_CHOICES,default='general', verbose_name="نطاق الفحص")
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=PROPERTY_LABELS['general_comment'])
    def __str__(self):
        return f"{self.key}"
    @property
    def folder_path(self):
        visit_id = str(self.visit.Request.visit_id)
        area_id = str(self.id)
        return f"Visit/{visit_id}/{area_id}"



class AreaImage(models.Model):
    area = models.ForeignKey(InspectionArea, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=general_report_image_upload_path)







class InspectionItem(models.Model):
    area = models.ForeignKey(InspectionArea, on_delete=models.CASCADE, related_name="items")
    key = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name=ITEM_LABELS["key"])
    is_available = models.BooleanField(default=True)

    score = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    @property
    def folder_path(self):
        visit_id = str(self.area.visit.Request.visit_id)
        area_id = str(self.area.id)
        item_key = str(self.key)
        return f"Visit/{visit_id}/{area_id}/{item_key}/"






def inspection_item_image_upload_path(instance, filename):
    return os.path.join(instance.item.folder_path, filename)


class InspectionItemImage(models.Model):
    item = models.ForeignKey(InspectionItem,on_delete=models.CASCADE,related_name="images",)
    image = models.ImageField(upload_to=inspection_item_image_upload_path)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)