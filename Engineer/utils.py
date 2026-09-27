from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from Admin.models import EmailSystemSettings
from django.core.mail.backends.console import EmailBackend
from .constants import ENGINEER_PATH as PATH
def send_custom_otp_email(recipient_email, otp_code):
    config = EmailSystemSettings.objects.first()

    if not config:
        return False
    connection = get_connection(
        backend=config.smtp_host,
        host=config.smtp_host,
        port=config.smtp_port,
        username=config.email_user,
        password=config.email_password,
        use_tls=True
    )

    context = {
    #    'engineer_name': engineer_name,
        'otp_code': otp_code,
        'subject': config.email_subject,
        'body_text': config.email_body,
        'footer_name': config.company_name,
    }

    html_content = render_to_string(PATH['VERIFY_OTP'], context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=config.email_subject,
        body=text_content,
        from_email=config.email_user,
        to=[recipient_email],
        connection=connection
    )
    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error logic: {e}")
        return False

from Client.models import WalletTransaction

import random


def mock_bank_transfer(amount, iban=None):
    # نحاكي تأخير بسيط
    import time

    time.sleep(1)

    # نجاح أو فشل عشوائي
    success = random.choice([True, True, True, False])

    if success:
        return {
            "status": "success",
            "transaction_id": f"MOCK-{random.randint(1000,9999)}",
        }

    return {"status": "failed", "message": "Bank rejected transfer"}


import os
import io
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from pypdf import PdfReader, PdfWriter
from django.core.files.base import ContentFile


def check_and_compress_file(new_input_file, file='bdf', quality=60):
    if not new_input_file:
        return False, "no_file"

    ext = os.path.splitext(new_input_file.name)[1].lower()
    valid_image_extensions = [".jpg", ".jpeg", ".png", ".webp"]
    new_file_name = os.path.basename(new_input_file.name)

    if ext == ".pdf" and file == "bdf":

        try:
            content = new_input_file.read()

            new_input_file.seek(0)

            malicious_signs = [b"/JS", b"/JavaScript", b"/AA", b"/OpenAction"]

            if any(tag in content for tag in malicious_signs):
                return False, "insecure"

            reader = PdfReader(io.BytesIO(content))

            writer = PdfWriter()

            reader = PdfReader(BytesIO(content))
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            for page in writer.pages:
                try:
                    page.compress_content_streams()
                except Exception:
                    pass

            buffer = BytesIO()
            writer.write(buffer)
            buffer.seek(0)

            processed_file = ContentFile(buffer.read(), name=new_file_name)

            return True, processed_file
        except Exception:
            return False, "harmony"

    elif ext in valid_image_extensions and file == "image":
        try:
            with Image.open(new_input_file) as img:
                img.verify()
            new_input_file.seek(0)
        except (IOError, SyntaxError, UnidentifiedImageError):
            return False, "invalid_image"

        try:
            with Image.open(new_input_file) as img:
                img = img.convert("RGB")
                buffer = BytesIO()
                img.save(buffer, format="JPEG", quality=quality, optimize=True)
            buffer.seek(0)

            processed_file = ContentFile(buffer.read(), name=new_file_name)
            return True, processed_file
        except Exception:
            return False, "harmony"

    else:
        return False, "unsupported"

















def create_or_reactivate_transaction(Order, Wallet, Amount):
    transaction = WalletTransaction.objects.filter(order=Order,wallet=Wallet,status="cancel").last()
    if transaction:
        transaction.amount = Amount
        transaction.status = "pending"
        transaction.cancelled_at = None
        transaction.save()
    else:
        transaction = WalletTransaction.objects.create(order=Order,wallet=Wallet,amount=Amount,status="pending")
    return transaction