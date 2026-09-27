from autobahn.wamp.gen.wamp.proto import TransportChannelFraming
from django import forms
from .models import Order, UserPhone, VisitDetails
from Admin.models import WorkDay
from django.core.exceptions import ValidationError
from config import StyledFormMixin
from django import forms
import bleach
from django import forms
from .models import ConsultationDetails, WorkDay
from django import forms
from .models import VisitDetails
from datetime import date, timedelta
from django import forms
from django.utils.safestring import mark_safe

from django import forms
from .models import UserPhone

from django import forms
from .models import UserPhone


class PhoneForm(forms.ModelForm):
    otp = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control-glass",
                "placeholder": "رمز التحقق",
                "autocomplete": "off",
                "maxlength": "4",
            }
        ),
    )

    class Meta:
        model = UserPhone
        fields = ["phone"]
        widgets = {
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control-glass",
                    "placeholder": "05xxxxxxxx",
                    "required": "required",
                    "autocomplete": "off",
                    "maxlength": "10",
                }
            )
        }

    def clean(self):
        if "send_otp" in self.data.values():
            phone = self.cleaned_data.get("phone")
            if not phone or not phone.isdigit() or len(phone) != 10 or not phone.startswith("05"):
                raise ValidationError("")
        elif "verify_otp" in self.data.values():
            otp = self.cleaned_data.get("otp")
            if not otp or not otp.isdigit() or len(otp) != 4:

                raise ValidationError("")
        return self.cleaned_data


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# class PropertyTypeWidget(forms.Widget):
#     def render(self, name, value, attrs=None, renderer=None):

#         is_apartment = "checked" if value == "apartment" else ""
#         is_villa = "checked" if value == "villa" else ""


#         return mark_safe(
#         f"""
#         <div class="property-options">
#           <label class="property-item" onclick="calculate()">
#             <input type="radio" id="apartment" name="{name}" value="apartment" {is_apartment}>
#             <div class="property-card-item">
#               <i class="far fa-house-building"></i>
#               <span>شقة / طابق</span>
#               <div class="property-check"><i class="fas fa-check"></i></div>
#             </div>
#           </label>


#           <label class="property-item" onclick="calculate()">
#             <input type="radio" id="villa" name="{name}" value="villa" {is_villa}>
#             <div class="property-card-item">
#               <i class="far fa-house-tree"></i>
#               <span>فيلا / دوبلكس</span>
#               <div class="property-check"><i class="fas fa-check"></i></div>
#             </div>
#           </label>
#         </div>
#     """
#     )
class PropertyTypeWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        str_value = str(value) if value is not None else ""

        is_apartment = "checked" if str_value == "1" else ""
        is_villa = "checked" if str_value == "2" else ""

        return mark_safe(
            f"""
        <div class="property-options">
          <label class="property-item">
            <input type="radio" id="apartment" name="{name}" value="1" {is_apartment}>
            <div class="property-card-item">
              <i class="far fa-house-building"></i>
              <span>شقة / طابق</span>
              <div class="property-check">
              <i class="fa-solid fa-check-double"></i>
              </div>
            </div>
          </label>

          <label class="property-item">
            <input type="radio" id="villa" name="{name}" value="2" {is_villa}>
            <div class="property-card-item">
              <i class="far fa-house-tree"></i>
              <span>فيلا / دوبلكس</span>
              <div class="property-check">
              <i class="fa-solid fa-check-double"></i>
              </div>
            </div>
          </label>
        </div>
        """
        )


class InspectionTypeWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):

        str_value = str(value) if value is not None else ""

        is_basic = "checked" if str_value == "1" else ""
        is_advanced = "checked" if str_value == "2" else ""

        return mark_safe(
            f"""
    <div class="services-grid">

        <!-- الباقة الأساسية -->
        <label class="service-card">
            <input type="radio" id="inspection_1" name="{name}" value="1" {is_basic} style="position:absolute; opacity:0; width:0; height:0;">

            <p class="service-title">فحص أساسي</p>

            <ul class="feature-list">
                <li class="feature-item">
                    <span>مهندس سعودي معتمد</span>
                    <i class="fas fa-check-circle icon-success"></i>
                </li>
                <li class="feature-item">
                    <span>فحص شامل لجميع أجزاء العقار</span>
                    <i class="fas fa-check-circle icon-success"></i>
                </li>
                <li class="feature-item">
                    <span>مطابقة القياسات الهندسية</span>
                    <i class="fas fa-check-circle icon-success"></i>
                </li>
                <li class="feature-item">
                    <span>مراجعة مستندات العقار</span>
                    <i class="fas fa-check-circle icon-success"></i>
                </li>
                <li class="feature-item">
                    <span>تقرير تفصيلي يوضح العيوب</span>
                    <i class="fas fa-check-circle icon-success"></i>
                </li>
                <li class="feature-item item-disabled">
                    <span>توثيق جميع أجزاء العقار</span>
                    <i class="fas fa-times-circle icon-danger"></i>
                </li>
                <li class="feature-item item-disabled">
                    <span>فرز الملاحظات حسب الغرف والتصنيف</span>
                    <i class="fas fa-times-circle icon-danger"></i>
                </li>
            </ul>

            <div class="total-price-wrapper">
                <div class="price-label">إجمالي تكلفة الخدمة</div>
                <div class="price-display">
                    <span class="total-price" id="normal_price">0</span>
                    <small class="icon-saudi_riyal"></small>
                </div>
                <small class="vat-note">شامل ضريبة القيمة المضافة</small>
            </div>
        </label>

        <!-- الباقة المتقدمة -->
        <label class="service-card card-advanced" >

            <input type="radio" id="inspection_2" name="{name}" value="2" {is_advanced} style="position:absolute; opacity:0; width:0; height:0;">

            <p class="service-title">فحص متقدم</p>

            <ul class="feature-list">
                <li class="feature-item">
                    <span>مهندس سعودي معتمد</span>
                    <i class="fas fa-check-circle icon-success"></i>
                </li>
                <li class="feature-item">
                    <span>فحص شامل لجميع أجزاء العقار</span>
                    <i class="fas fa-check-circle icon-success"></i>
                </li>
                <li class="feature-item">
                    <span>مطابقة القياسات الهندسية</span>
                    <i class="fas fa-check-circle icon-success"></i>
                </li>
                <li class="feature-item">
                    <span>مراجعة مستندات العقار</span>
                    <i class="fas fa-check-circle icon-success"></i>
                </li>
                <li class="feature-item">
                    <span>تقرير تفصيلي يوضح العيوب</span>
                    <i class="fas fa-check-circle icon-success"></i>
                </li>
                <li class="feature-item item-highlighted">
                    <span>توثيق جميع أجزاء العقار</span>
                    <i class="fas fa-check-circle icon-success"></i>
                </li>
                <li class="feature-item item-highlighted">
                    <span>فرز الملاحظات حسب الغرف والتصنيف</span>
                    <i class="fas fa-check-circle icon-success"></i>
                </li>
            </ul>

            <div class="total-price-wrapper">
                <div class="price-label">إجمالي تكلفة الخدمة</div>
                <div class="price-display">
                    <span class="total-price" id="full_price">0</span>
                    <small class="icon-saudi_riyal"></small>
                </div>
                <small class="vat-note">شامل ضريبة القيمة المضافة</small>
            </div>
        </label>

    </div>
        """
        )


class BaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update(
                    {"class": "form-control glass-input form-select form-label"}
                )
            else:
                field.widget.attrs.update(
                    {"class": "form-control glass-input form-label"}
                )


def apply_field_styles(fields, errors, excluded_fields=None):
    if excluded_fields is None:
        excluded_fields = []

    for name in fields:
        if name in excluded_fields:
            continue

        field = fields[name]
        existing = field.widget.attrs.get("class", "")

        classes = f"{existing} write".strip()

        if name in errors:
            classes += " error"

        field.widget.attrs["class"] = classes


class VisitDetailsForm(forms.ModelForm):
    class Meta:
        model = VisitDetails
        fields = [
            "name",
            "phone",
            "city",
            "property_type",
            "inspection_type",
            "neighborhood",
            "property_size",
            "day",
            "time_slot",
        ]

        widgets = {
            "property_size": forms.NumberInput(
                attrs={
                    "class": "area-input run-property",
                    "placeholder": "200",
                    "min": 30,
                    "required": True,
                    "id": "property_size",
                }
            ),
            "property_type": PropertyTypeWidget(),
            "inspection_type": InspectionTypeWidget(),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control glass-input form-label",
                    "placeholder": "أدخل الاسم..",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control form-label",
                    "placeholder": "05xxxxxxxx",
                }
            ),
            "city": forms.Select(
                attrs={
                    "class": "live-cities form-control glass-input form-select form-label",
                }
            ),
            "neighborhood": forms.TextInput(
                attrs={
                    "class": "form-control form-label",
                }
            ),
            "time_slot": forms.Select(
                attrs={
                    "class": "form-control form-label",
                    "id": "time-slots-select",
                    "disabled": "disabled",
                }
            ),
            "day": forms.DateInput(
                attrs={
                    "class": "form-control form-label",
                    "id": "visit-day",
                    "autocomplete": "off",
                    "readonly": "readonly",
                    "placeholder": "اختر التاريخ المناسب للفحص...",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get("day")
        property_size = cleaned_data.get("property_size")
        if not property_size or property_size < 10:
            raise ValidationError({"property_size": "invalid"})
        if not day or day < date.today():
            raise ValidationError({"day": "invalid"})
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        apply_field_styles(
            self.fields,
            self.errors,
            excluded_fields=["property_size", "property_type", "inspection_type"],
        )


class ConsultationForm(BaseForm, forms.ModelForm):
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = ConsultationDetails
        fields = ["name", "phone", "summary", "work_time", "work_day", "work_history"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "أدخل الاسم..",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "05xxxxxxxx",
                }
            ),
            "summary": forms.Textarea(
                attrs={
                    "placeholder": "أدخل الملخص..",
                }
            ),
            "work_history": forms.DateInput(
                attrs={
                    "type": "text",
                    "id": "calendar",
                    "placeholder": "اختر التاريخ..",
                }
            ),
            "work_time": forms.Select(
                attrs={
                    "id": "time_select",
                    "disabled": "disabled",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        # 1) work_time
        work_time = cleaned_data.get("work_time")
        if not work_time or work_time == "...":
            raise ValidationError({"work_time": "invalid"})
        # 2) work_history
        work_history = cleaned_data.get("work_history")
        if not work_history or work_history < date.today():
            raise ValidationError({"work_history": "invalid"})
        day_number = ((work_history.weekday() + 1) % 7) + 1
        try:
            work_day = WorkDay.objects.get(number=day_number)
            if not work_day.is_working:
                raise ValidationError({"work_history": "invalid"})
            cleaned_data["work_day"] = work_day.name_ar
            cleaned_data["price"] = work_day.total_price

        except WorkDay.DoesNotExist:
            raise ValidationError({"work_history": "invalid"})
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        apply_field_styles(self.fields, self.errors)
