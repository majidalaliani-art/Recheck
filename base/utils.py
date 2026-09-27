from io import BytesIO
from django.core.files.base import ContentFile
import os
from Admin.models import ContactMethod, PaymentMethod
from Engineer.models import Engineer
from PIL import Image, UnidentifiedImageError
from django.templatetags.static import static

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


def is_file_duplicate(obj, field_name, new_file):
    current_file = getattr(obj, field_name, None)
    if not current_file or not current_file.name:
        return False

    try:
        existing_file_name = os.path.basename(current_file.name).strip()
        incoming_file_name = os.path.basename(new_file.name).strip()

        if existing_file_name == incoming_file_name:
            return True

    except Exception as e:
        # print(f"Error checking name: {e}")
        pass

    return False


def process_and_replace_image(obj, field_name, new_input_file, quality=60):

    if is_file_duplicate(obj, field_name, new_input_file):
        return False

    valid_extensions = [".jpg", ".jpeg", ".png", ".webp"]
    ext = os.path.splitext(new_input_file.name)[1].lower()
    if ext not in valid_extensions:
        return False

    try:
        with Image.open(new_input_file) as img:
            img.verify()
        new_input_file.seek(0)

    except (IOError, SyntaxError, UnidentifiedImageError):
        return False

    else:
        try:
            with Image.open(new_input_file) as img:
                img = img.convert("RGB")
                buffer = BytesIO()
                img.save(buffer, format="JPEG", quality=quality, optimize=True)
            buffer.seek(0)

            new_file_name = os.path.basename(new_input_file.name)
            processed_file = ContentFile(buffer.read(), name=new_file_name)

            old_file = getattr(obj, field_name, None)
            if old_file and hasattr(old_file, "path"):
                if os.path.exists(old_file.path):
                    old_file.delete(save=False)

            setattr(obj, field_name, processed_file)
            obj.save()

            return True
        except Exception:
            return False






def global_data(request):
    contacts = ContactMethod.objects.all().values("key", "link", "user", "is_active")
    Payment = PaymentMethod.objects.all().values("key", "name", "is_active")
    if request.user.is_authenticated:
        engineer = User.objects.filter(id=request.user.id).values("username", "first_name", "last_name").first()
        staff_profile = getattr(request.user, 'staff_profile', None)
        try:
            if request.user.staff_profile.avatar and request.user.staff_profile.avatar.url:
                engineer['avatar'] = request.user.staff_profile.avatar.url
            else:
                engineer['avatar'] = static('Style/images/staff.jpg')
        except Exception:
            engineer['avatar'] = static('Style/images/staff.jpg')
    else:
        avatar = static("Style/images/staff.jpg")
        engineer = {'avatar':avatar,"username": None, "first_name": None, "last_name": None}

    return {"contacts": contacts, "payment": Payment, "engineer": engineer}
