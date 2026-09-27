from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Engineer
from django.db import models
from schwifty import IBAN
import re
from .models import EngineerApplication
from PIL import Image
from config import StyledFormMixin
from django.core.cache import cache
from django.utils.safestring import mark_safe
from .utils import check_and_compress_file
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class FormStylingMixin:

    STAR_FIELDS = ["city"]

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


# class EmailVerificationForm(FormStylingMixin, forms.Form):
#     email = forms.EmailField(required=True)

#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get("email")
#         email_regex = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"
#         if email and not re.match(email_regex, email):
#             self.add_error("email", "")


class ApplyViewForm(StyledFormMixin, FormStylingMixin, forms.ModelForm):
    class Meta:
        model = EngineerApplication
        fields = [
            "full_name_ar",
            "full_name_en",
            "phone",
            "years_of_experience",
            "secondary_phone",
            "sce_number",
            "city",
            "email",
            "iban_number",
            "iban_proof",
            "university_degree",
            "sce_membership",
            "cv_file",
            "equipment_photos",
        ]
        widgets = {
            "city": forms.Select(
                attrs={
                    "class": "text-center live-cities form-control glass-input form-select form-label",
                }
            ),
            "phone": forms.TextInput(attrs={"dir": "ltr"}),
            "secondary_phone": forms.TextInput(attrs={"dir": "ltr"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields_to_clear = [
            "iban_proof",
            "university_degree",
            "sce_membership",
            "cv_file",
            "equipment_photos",
        ]

        for field_name, field in self.fields.items():
            if field_name in fields_to_clear:
                field.widget.attrs["class"] = ""

    def clean(self):
        cleaned_data = super().clean()
        for field_name in list(cleaned_data.keys()):
            value = cleaned_data.get(field_name)

            try:
                field_type = self.instance._meta.get_field(field_name)
            except:
                continue
            if field_name == "city" and not value:
                self.add_error(field_name, "")

            if field_name == "iban_number":
                try:
                    IBAN(value)
                except ValueError:
                    self.add_error(field_name, "")

            if isinstance(field_type, (models.FileField, models.ImageField)):
                if value and hasattr(value, 'name') and value.name.lower().endswith('.pdf'):
                    success, result = check_and_compress_file(value)
                    if success:
                        cleaned_data[field_name] = result
                    else:
                        if result == "insecure":
                            self.add_error(field_name, "تم رفض الملف! يحتوي على برمجيات أو روابط غير آمنة.")
                        elif result == "unsupported":
                            self.add_error(field_name, "صيغة الملف غير مدعومة.")
                        elif result == "invalid_image":
                            self.add_error(field_name, "الملف المرفوع ليس صورة صالحة أو تالفة.")
                        else:
                            self.add_error(field_name, "حدث خطأ أثناء معالجة الملف وضغطه.")

        return cleaned_data


from django import forms
from django.contrib.auth import get_user_model

User = get_user_model() # يجيب موديل المستخدم المعتمد في المشروع
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class RegisterForm(StyledFormMixin, FormStylingMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.TextInput(attrs={'class': 'form-control glass-input form-label text-center', 'placeholder': 'أدخل كلمة السر'})
        self.fields['password2'].widget = forms.TextInput(attrs={'class': 'form-control glass-input form-label text-center', 'placeholder': 'أعد إدخال كلمة السر'})
        self.fields['email'].disabled = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
