

# --- الأقسام في لوحة التحكم (Admin Sections) ---
ADMIN_SECTIONS = {
    "PERSONAL": "👤 البيانات الشخصية والتواصل",
    "DEGREE": "🎓 الشهادة الجامعية",
    "SCE": "📜 هيئة المهندسين (SCE)",
    "CV": "📄 السيرة الذاتية (CV)",
    "EQUIPMENT": "🛠️ المعدات والأجهزة",
    "FINAL": "✅ القرار النهائي",
}

# --- الإجراءات الجماعية (Admin Actions) ---
ADMIN_ACTIONS = {
    "APPROVE": "تفعيل المهندسين المحددين",
    "SUSPEND": "إيقاف المهندسين المحددين",
}

# --- نصوص الموديل (Model Labels) ---
MODEL_LABELS = {
    "FULL_NAME_AR": "الاسم بالكامل (عربي)",
    "FULL_NAME_EN": "Full Name (English)",
    "EMAIL": "البريد الإلكتروني",
    "PHONE": "رقم الجوال الأساسي",
    "SECONDARY_PHONE": "رقم الجوال الثانوي",
    "CITY": "المدينة",
    "IBAN": "رقم الآيبان (IBAN)",
    "STATUS": "الحالة",
    "NOTES": "ملاحظات",
    "DEGREE": "الشهادة",
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

INSPECTION_CHOICES = [
    ('standard', 'فحص عادي'),
    ('comprehensive', 'فحص شامل'),
]


STATUS_DICT = {
        'null': 'لا يوجد',
        'pending': 'الطلب متاح',
        'in_progress': 'بدء الفحص',
        'report_submitted': 'تسليم التقرير',
        'under_review': 'تحت المراجعة',
        'approved': 'تم اعتماد التقرير ✅',
    }
my_status_list = ['in_progress', 'report_submitted', 'under_review', 'approved']
