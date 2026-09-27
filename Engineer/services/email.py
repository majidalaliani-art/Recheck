from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .constants import PATH
from django.contrib.auth import get_user_model
User = get_user_model()

def send_otp_email(recipient_email, otp):
    subject = "كود التحقق لإعادة تعيين كلمة المرور"
    recipient = [recipient_email]
    user = User.objects.filter(email=recipient_email).first()
    if user:
        username = user.username
        first_name = user.first_name if user.first_name else "عميلنا العزيز"
    else:
        username = "User"
        first_name = "عميلنا العزيز"


    context = {
        "username": username,
        "name": first_name,
        "otp": otp,
    }


    html_content = render_to_string(PATH["VERIFY_OTP"], context)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, None, recipient)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
