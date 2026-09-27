
from django import forms
from .models import VisitReport
from django.utils.safestring import mark_safe

class FormStylingMixin:
    STAR_FIELDS = [
        "date",
        "time",
        "neighborhood",
        "unit_number",
        "number_of_floors",
        "detailed_address",
        "latitude",
        "longitude",
        "property_image",
        "city",
        "requestType",
        "propertyType",
        "property_condition",
        # "property_owner",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get("class", "")
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = (
                    f"{existing_classes} form-check-input".strip()
                )
            else:
                new_input_classes = f"{existing_classes} custom-field-box"
                if field.widget.attrs.get("readonly") or field.disabled:
                    new_input_classes += "pre-filled"
                field.widget.attrs["class"] = new_input_classes.strip()
            if field.label:
                label_html = f'<label class="form-label">{field.label}'
                if field.required or field_name in self.STAR_FIELDS:
                    label_html += '<span class="text-danger"> *</span>'
                label_html += "</label>"
                field.label = mark_safe(label_html)


class VisitReportForm(FormStylingMixin, forms.ModelForm):
    city = forms.CharField(
        label="المدينة",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-contro","readonly": "readonly",}),)
    requestType = forms.CharField(
        label="نوع الطلب",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-contro","readonly": "readonly",}),)
    propertyType = forms.CharField(
        label="نوع العقار",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-contro","readonly": "readonly",}),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        status = getattr(self.instance.Request, 'status', None)

        self.fields["time"].input_formats = ["%H:%M"]
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "toggle-switch"})
                if status != "in_progress":
                    current_classes = field.widget.attrs.get("class", "")
                    field.widget.attrs["class"] = f"{current_classes} this_bdf".strip()
                field.label_suffix = ""


                field.label = mark_safe(f'<label class="custom-label">{field.label}</label>')
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({"class": "d-none"})
            elif not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": f"form-control  shadow-sm border-2 rounded-3"})
                if status != "in_progress":
                    current_classes = field.widget.attrs.get("class", "")
                    field.widget.attrs["class"] = f"{current_classes} this_bdf".strip()
                field.label_suffix = ""
                field.label = mark_safe(f'<label class="custom-label">{field.label}</label>')

        if self.instance and self.instance.pk:
            for field_name in ['building_area_sqm']:
                if field_name in self.initial and self.initial[field_name] is not None:
                    val = self.initial[field_name]
                    try:
                        if float(val).is_integer():
                            self.initial[field_name]  = int(float(val))
                    except (ValueError, TypeError):
                        pass


    class Meta:
        model = VisitReport
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            "time": forms.TimeInput(attrs={"type": "time",},format="%H:%M",),
            }



class panel_1_Form(FormStylingMixin, forms.ModelForm):
    class Meta:
        model = VisitReport
        fields = [
            "date",
            "time",
            "neighborhood",
            "unit_number",
            "detailed_address",
            "latitude",
            "longitude",
            "property_image",
        ]


class panel_2_Form(FormStylingMixin, forms.ModelForm):
    class Meta:
        model = VisitReport
        fields = [
            "building_activity",
            "property_condition",
            "property_owner",
            "number_of_floors",
            "building_license_number",
            "property_developer",
            "design_office",
            "engineering_supervisor",
            "electricity_meter_reading",
            "water_meter_reading",
            "property_age_years",
            "building_area_sqm",
            "electricity_meter_number",
            "water_meter_number",
            # 1
            "street_north",
            "street_south",
            "street_east",
            "street_west",
            # 2
            "building_north",
            "building_south",
            "building_east",
            "building_west",
            # 3
            "infra_electricity",
            "infra_water",
            "infra_sewage",
            "infra_asphalt",
            "infra_lighting",
            "infra_network",
            # 4
            "feat_disabled_friendly",
            "feat_fire_system",
            "feat_garden",
            "feat_parking",
            "feat_skylight",
            "feat_pool",
            "feat_elevator",
            "feat_cameras",
            "feat_central_ac",
            "feat_water_tanks",
            "feat_outdoor_seating",
            # 5

            "doc_building_license",
            "doc_soil_test",
            "doc_structural_warranty",
            "doc_architectural_plans",
            "doc_structural_plans",
            "doc_electrical_plans",
            "doc_mechanical_plans",
            "doc_survey_form",
            "doc_eng_supervision",
            "doc_finishes_warranty",
            "doc_rebar_report",

        ]
