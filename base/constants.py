# # --- الأقسام في لوحة التحكم (Admin Sections) ---
# ADMIN_SECTIONS = {
#     "PERSONAL": "👤 البيانات الشخصية والتواصل",
#     "DEGREE": "🎓 الشهادة الجامعية",
#     "SCE": "📜 هيئة المهندسين (SCE)",
#     "CV": "📄 السيرة الذاتية (CV)",
#     "EQUIPMENT": "🛠️ المعدات والأجهزة",
#     "FINAL": "✅ القرار النهائي",
# }

# # --- الإجراءات الجماعية (Admin Actions) ---
# ADMIN_ACTIONS = {
#     "APPROVE": "تفعيل المهندسين المحددين",
#     "SUSPEND": "إيقاف المهندسين المحددين",
# }

# # --- نصوص الموديل (Model Labels) ---
# MODEL_LABELS = {
#     "FULL_NAME_AR": "الاسم بالكامل (عربي)",
#     "FULL_NAME_EN": "Full Name (English)",
#     "EMAIL": "البريد الإلكتروني",
#     "PHONE": "رقم الجوال الأساسي",
#     "SECONDARY_PHONE": "رقم الجوال الثانوي",
#     "CITY": "المدينة",
#     "IBAN": "رقم الآيبان (IBAN)",
#     "STATUS": "الحالة",
#     "NOTES": "ملاحظات",
#     "DEGREE": "الشهادة",
#     "SCE": "العضوية",
#     "CV": "السيرة الذاتية",
#     "EQUIPMENT": "صور الأجهزة",
# }

# # --- خيارات الحالة (Choices) ---
# FILE_STATUS_CHOICES = [
#     ('required', 'مطلوب'),
#     ('pending', 'قيد المراجعة'),
#     ('accepted', 'مقبول'),
#     ('rejected', 'مرفوض'),
# ]

# INSPECTION_CHOICES = [
#     ('standard', 'فحص عادي'),
#     ('comprehensive', 'فحص شامل'),
# ]


# STATUS_DICT = {
#         'null': 'لا يوجد',
#         'pending': 'الطلب متاح',
#         'in_progress': 'بدء الفحص',
#         'report_submitted': 'تسليم التقرير',
#         'under_review': 'تحت المراجعة',
#         'approved': 'تم اعتماد التقرير ✅',
#     }


# CLIENTKEY = {
#     "LOGIN": 'Client/login.html',  # User login via phone number

#     'HOMEPAGE': 'Client/homepage.html',  # Homepage of the site
#     'VILLA':'Client/villa.html',
#     'BUYING' :'Client/buying.html',
#     # 'APARTMENT':'',
#     'OTP_TTL':5 * 60, # 5 minutes in seconds
#     'OTP_RESEND_DELAY': 60 , # Waiting time before requesting a new OTP: 60 seconds
#     'MAX_ATTEMPTS'  :5 , # Maximum number of OTP requests allowed
#     'ATTEMPT_WINDOW' : 60, # Time window in seconds (1 minute)
#     'OTP': 4,  # Number of digits for the OTP
#     'MAX_ATTEMPTS': 5,       # Maximum allowed OTP requests per IP
#     'WINDOW': 0 , # Time window in seconds to count attempts
# }

# ENGINEERKEY_PATH = {
#     'LOGIN': 'Engineer/login.html',
#     'SIGNUP': 'Engineer/signup.html',
#     'VERIFY_OTP' : 'Engineer/otp_email.html',
#     'APPLY' : 'Engineer/apply.html',
#     'DASHBOARD' : 'Engineer/dashboard.html',
#     'LIST_ORDERS' : 'Engineer/homepage/orders_list.html',

# }


# VISITS_ENGINEERKEY_PATH = {
#     'START_VISIT' : 'Engineer/Visits/start_visit.html',
#     'VISIT_DETAIL' : 'Engineer/Visits/visit_detail.html',
# }


PATH = {
    "LOGIN":"registration/login.html",
    "TERMS": "base/terms.html",
    "PRIVACY": "base/privacy.html",
    "CANCELATION": "base/cancelation.html",
    "INSPECTOR": "base/Inspector.html",

        # صفحات نسيت/إعادة تعيين كلمة السر
    "PASSWORD_RESET": "registration/password_reset_form.html",
    "PASSWORD_RESET_DONE": "registration/password_reset_done.html",
    "PASSWORD_RESET_EMAIL": "registration/email/password_reset_email.html",
    "PASSWORD_RESET_SUBJECT": "registration/email/password_reset_subject.txt",

    "PASSWORD_RESET_CONFIRM": "registration/password_reset_confirm.html",
    "PASSWORD_RESET_COMPLETE": "registration/password_reset_complete.html",
}
