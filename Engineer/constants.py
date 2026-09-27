ENGINEER_PATH = {
    "APPLY": "Client/apply.html",
    "REGISTER": "Engineer/register.html",
    "SIGNUP": "Engineer/signup.html",
    "SETTINGS": "Engineer/settings.html",
    "DATA": "Engineer/data.html",
    "ORDERS_DISPLAY": "Engineer/Orders/Orders_Display.html",
    "IN_PROGRESS_ORDERS": "Engineer/Orders/in_progress_orders.html",
    "PROGRESS_ORDER": "Engineer/Orders/order_progress.html",
    "COMPLETED_ORDERS": "Engineer/Orders/completed_orders.html",
    "WALLET": "Engineer/Wallet.html",
    "LIST_ORDERS": "Engineer/homepage/orders_list.html",
}


# --- الأقسام في لوحة التحكم (Admin Sections) ---
ADMIN_SECTIONS = {
    "PERSONAL": "👤 البيانات الشخصية والتواصل",
    "DEGREE": "🎓 الشهادة الجامعية",
    "SCE": "📜 هيئة المهندسين (SCE)",
    "CV": "📄 السيرة الذاتية (CV)",
    "EQUIPMENT": "🛠️ المعدات والأجهزة",
    "FINAL": "✅ القرار النهائي",
    "BANKING": "بيانات الحساب البنكي",
}

# --- الإجراءات الجماعية (Admin Actions) ---
ADMIN_ACTIONS = {
    "APPROVE": "تفعيل المهندسين المحددين",
    "SUSPEND": "إيقاف المهندسين المحددين",
}

# --- نصوص الموديل (Model Labels) ---
MODEL_LABELS = {
    "FULL_NAME_AR": "الاسم بالكامل (عربي)",
    "FULL_NAME_EN": "لاسم بالكامل (English)",
    "EMAIL": "البريد الإلكتروني",
    "PHONE": "رقم الجوال الأساسي",
    "SECONDARY_PHONE": "رقم الجوال الثانوي",
    "CITY": "المدينة",
    "IBAN": "رقم الآيبان (IBAN)",
    "STATUS": "الحالة",
    "NOTES": "ملاحظات",
    "DEGREE": "الشهادة",
    "AVATAR": "الصورة الرمزية",
    "SCE": "العضوية",
    "CV": "السيرة الذاتية",
    "EQUIPMENT": "صور الأجهزة",
}

# --- خيارات الحالة (Choices) ---
FILE_STATUS_CHOICES = [
    ('required', 'مطلوب'),
    ('pending', 'قيد المراجعة'),
    ('accepted', 'مقبول'),
    ('rejected', 'مرفوض'),
]



STATUS_CHOICES = (
    ("success", "مقبول"),
    ('pending', 'قيد المراجعة'),
    ("rejected", "مرفوض"),
)
