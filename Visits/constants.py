# ===================================================================
# PATH
# ===================================================================
PATH = {
    "VISIT": "Services/Visit/VisitBase.html",
    "REVIEW": "Services/Visit/VisitBase.html",
    "REVIEW": "Services/VisitReview/Review.html",
}

# ===================================================================
# ARABIC LABELS DICTIONARY FOR FIELD VISIT
# ===================================================================
FIELD_VISIT_LABELS = {
    'order': 'الطلب المرتبط',
    'service_type': 'نوع العقار',
    'inspection_type': 'نوع الطلب',
    'engineer': 'المهندس المسؤول',
    'engineer_amount': 'مستحقات المهندس',
    'platform_amount': 'مستحقات المنصة',
    'tax_rate_amount': 'معدل الضريبة',
    'total_amount': 'المبلغ الإجمالي',
    'total_with_tax': 'المبلغ الإجمالي مع الضريبة',
    'is_null': 'سحب الطلب',
    'status': 'الحالة',
    'accepted_at': 'وقت القبول',
    'deadline': 'الموعد النهائي',
    'processed': 'تمت المعالجة',
    'created_at': 'تاريخ الإنشاء',
}

# ==========================================================
# PROPERTY INFORMATION MODEL

# 1. CHOICES TUPLES
ACTIVITY_CHOICES = [
    ('raw', 'سكني'),
    ('commercial', 'تجاري')
]

CONDITION_CHOICES = [
    ("furnished", "مشطب - مؤثث"),
    ("unfurnished", "مشطب - غير مؤثث"),
    ("raw", "عظم"),
]

# 2. LABELS DICTIONARY (Arabic Translations)

PROPERTY_LABELS = {
    "related_visit": "الزيارة المرتبطة",
    # The 3 specific fields you requested to extract
    "detailed_address": "العنوان التفصيلي",
    "latitude": "خط العرض",
    "longitude": "خط الطول",
    "property_image": "صورة العقار",
    "neighborhood": "الحي",
    "time": "الوقت",
    "date": "التاريخ",
    "unit_number": "رقم الوحدة",
    # General Info
    "building_activity": "نشاط البناء",
    "property_condition": "حالة العقار",
    "property_owner": "مالك العقار",
    "building_license_number": "رقم رخصة البناء",
    "property_developer": "المطور العقاري",
    "design_office": "المكتب المصمم",
    "engineering_supervisor": "المشرف الهندسي",
    # Utilities & Measurements
    "electricity_meter_number": "رقم عداد كهرباء",
    "electricity_meter_reading": "قراءة عداد الكهرباء",
    "water_meter_number": "رقم عداد الماء",
    "water_meter_reading": "قراءة عداد الماء",
    "property_age_years": "عمر العقار بالسنوات",
    "land_area_sqm": "مساحة الأرض (م²)",
    "building_area_sqm": "مسطحات البناء (م²)",  # أبو غازي
    "number_of_floors": "عدد الطوابق",
    # Neighbors (Boolean)
    "street_north": "شمالي",
    "street_south": "جنوبي",
    "street_east": "شرقي",
    "street_west": "غربي",
    # Buildings (Boolean) - إضافة العماير/البنايات
    "building_north": "شمالية",
    "building_south": "جنوبية",
    "building_east": "شرقية",
    "building_west": "غربية",
    # Infrastructure (Boolean)
    "infra_electricity": "مرفق كهرباء",
    "infra_water": "مرفق مياة",
    "infra_sewage": "صرف صحي",
    "infra_asphalt": "طرق أسفلت",
    "infra_lighting": "طرق منارة",
    "infra_network": "شبكة إتصال",
    # Features (Boolean)
    "feat_disabled_friendly": "صديق للمعاقين وكبار السن",
    "feat_fire_system": "نظام مكافحة الحرائق",
    "feat_garden": "حديقة داخلية",
    "feat_parking": "موقف السيارة (جراج)",
    "feat_skylight": "فتحة إنارة سقفية",
    "feat_pool": "مسبح (حمام سباحة)",
    "feat_elevator": "مصعد كهربائي",
    "feat_cameras": "كاميرات مراقبة",
    "feat_central_ac": "تكييف مركزي",
    "feat_water_tanks": "خزانات ماء أرضية",
    "feat_outdoor_seating": "جلسة خارجية",
    # Documents (Boolean)
    "doc_building_license": "رخصة البناء",
    "doc_soil_test": "تقرير فحص التربة",
    "doc_structural_warranty": "ضمان الهيكل الإنشائي",
    "doc_architectural_plans": "المخططات المعمارية",
    "doc_structural_plans": "المخططات الإنشائية",
    "doc_electrical_plans": "المخططات الكهربائية",
    "doc_mechanical_plans": "المخططات الميكانيكية",
    "doc_survey_form": "استمارة الرفع المساحي",
    "doc_eng_supervision": "شهادة إشراف مكتب هندسي",
    "doc_finishes_warranty": "شهادة ضمان التشطيبات",
    "doc_rebar_report": "تقرير استلام حديد التسليح",
    "general_comment": "تعليق عام",
}


AREA_CHOICES = [
    ("general", "تقرير عام"),
    ("bedroom", "غرفة نوم"),
    ("lounge", "صالة"),
    ("majlis", "مجلس"),
    ("bathroom", "دورة مياه"),
    ("kitchen", "مطبخ"),
    ("corridor", "ممر"),
    ("entrance", "مدخل"),
    ("warehouse", "مستودع"),
    ("laundry_room", "غرفة الغسيل"),
    ("balcony", "بلكونة"),
    ("roof", "سطح"),
    ("outdoor_areas", "المناطق الخارجية"),
    ("underground_water_tank", "الخزان الارضي"),
]


# ==========================================================


# Choices for the inspection items menu
CATEGORY_CHOICES = [
    ('electrical', 'الكهرباء'),
    ('plumbing', 'السباكة'),
    ('cracks', 'التشققات'),
    ('moisture', 'الرطوبة'),
    ('walls', 'الجدران والدهانات'),
    ('ceilings', 'الأسقف'),
    ('floors', 'الأرضيات'),
    ('hvac', 'التكييف'),
    ('doors', 'الأبواب'),
    ('windows', 'النوافذ'),
    ('waterproofing', 'العزل المائي'),
    ('insulation', 'العزل الحراري'),
    ('other', 'أخرى'),
]

INSPECTION_ITEMS = [
    {"slug": "electrical", "name_ar": "الكهرباء", "icon_class": "fas fa-bolt"},
    {"slug": "plumbing", "name_ar": "السباكة", "icon_class": "fas fa-faucet"},
    {"slug": "cracks", "name_ar": "التشققات", "icon_class": "fas fa-house-damage"},
    {"slug": "moisture", "name_ar": "الرطوبة", "icon_class": "fas fa-tint"},
    {"slug": "walls", "name_ar": "الجدران والدهانات", "icon_class": "fas fa-border-all"},
    {"slug": "ceilings", "name_ar": "الأسقف", "icon_class": "fas fa-arrow-up"},
    {"slug": "floors", "name_ar": "الأرضيات", "icon_class": "fas fa-layer-group"},
    {"slug": "hvac", "name_ar": "التكييف", "icon_class": "fas fa-snowflake"},
    {"slug": "doors", "name_ar": "الأبواب", "icon_class": "fas fa-door-closed"},
    {"slug": "windows", "name_ar": "النوافذ", "icon_class": "fas fa-window-restore"},
    {"slug": "waterproofing", "name_ar": "العزل المائي", "icon_class": "fas fa-umbrella"},
    {"slug": "insulation", "name_ar": "العزل الحراري", "icon_class": "fas fa-temperature-high"},
    {"slug": "other", "name_ar": "أخرى", "icon_class": "fas fa-ellipsis-h"},
]





# Dictionary for General Section labels
GENERAL_LABELS = {
    'overall_rating': "التقييم العام للعقار",
    'overall_description': "الوصف العام للحالة",
    'general_photo': "صورة عامة للمبنى",
}

# Dictionary for Card and Note labels
INSPECTION_LABELS = {
    'category': "الصنف (المنيو)",
    'rating': "تقييم الصنف",
    'note_text': "وصف الملاحظة",
    'note_image': "صورة الملاحظة",
}


# ==========================================================
# Add this to your existing dictionary
ROOM_LABELS = {
    'room_name': "اسم الغرفة / الوحدة",
}


VISIT_ITEM_LABELS = {
    "visit": "الزيارة",
    "title": "اسم البند العام",
    "has_score": "تفعيل النسبة",
    "score": "النسبة",
    "image": "الصورة",
    "comment": "شرح الصورة",
}


# ////////////  Room Model ////////////

# Unified dictionary for Room, Item, and Image labels
ROOM_ITEM_LABELS = {
    # Room-level labels
    "name": "اسم الغرفة",
    "description": "توضيح موقع الغرفة",
    "visit": "الزيارة الميدانية",
    "created_at": "تاريخ الإنشاء",
    # Item-level labels
    "title": "اسم البند",
    "room": "الغرفة",
    "has_score": "هل يوجد تقييم؟",
    "score": "نسبة التقييم (%)",
    # Image-level labels (The Image + Text Box)
    "item": "البند التابع له",
    "image": "الصورة",
    "comment": "شرح الصورة (الملاحظة)",
}



#
# قاموس للنصوص والتسميات
ITEM_LABELS = {
    "key": "البند",
    "score": "نسبة التقييم (%)",
    "score_help": "أدخل قيمة بين 0 و 100",
}
