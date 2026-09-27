PATH = {
    "BASE": "Client/CientBase.html",
    "LOGIN": "Client/Login.html",  # User login via phone number
    "HOMEPAGE": "Client/Homepage.html",  # Homepage of the site
    "PROPERTY": "Client/Property.html",
    "BOOKING": "Client/Booking.html",
    "ORDER": "Client/Order.html",
    "CONSULTATION": "Client/consultation.html",
    "ORDERS": "Client/Orders.html",
    # 'APARTMENT':'',
    "OTP_TTL": 5 * 60,  # 5 minutes in seconds
    "OTP_RESEND_DELAY": 60,  # Waiting time before requesting a new OTP: 60 seconds
    "MAX_ATTEMPTS": 5,  # Maximum number of OTP requests allowed
    "ATTEMPT_WINDOW": 60,  # Time window in seconds (1 minute)
    "OTP": 4,  # Number of digits for the OTP
    "MAX_ATTEMPTS": 5,  # Maximum allowed OTP requests per IP
    "WINDOW": 0,  # Time window in seconds to count attempts
}

PAYMENT_STATUS = {
    "pending": "قيد الانتظار",
    "success": "تم الدفع بنجاح",
    "failed": "فشل الدفع",
    "cancel": "تم إلغاؤه",

}

CONSULTATION_STATUS = {
    "waiting": "قيد الانتظار",
    "published": "تم النشر",
    "in_progress": "جاري الفحص",
    "under_review": "جاري المراجعة",
    "completed": "تم الانتهاء",
}

ORDER_STATUS = {
    "waiting": "قيد الانتظار",
    "published": "تم النشر",
    "in_progress": "جاري الفحص",
    "under_review": "جاري المراجعة",
    "completed": "تم الانتهاء",
}


ORDER_TYPES = (
    ("visit", "زيارة"),
    ("consultation", "استشارة"),
)


##########################################################################
PAYMENT_LABELS = {
    "order": "الطلب",
    "amount": "المبلغ الإجمالي",
    "tax_amount": "الضريبة",
    "net_amount": "المبلغ بعد الضريبة",
    "engineer_amount": "نصيب المهندس",
    "platform_amount": "نصيب المنصة",
    "status": "حالة الدفع",
    "created_at": "تاريخ الإنشاء",
    "updated_at": "تاريخ التحديث",
}


TIME_SLOTS = {
    "morning": "فترة الصباح",
    "noon": "فترة الظهر",
    "evening": "فترة العصر",
    "engineer": "حسب التنسيق مع المهندس",
}


LOCK_TIME = 5

##########################################################################

TRANSACTION_STATUS = (
    ("pending", "معلق (قيد العمل)"),
    ("completed", "مكتمل (رصيد متاح)"),
    ("withdraw", "تم السحب"),
    ("cancel", "ملغي"),
)



TRANSACTION_TYPES = (
        ("deposit", "إيداع أرباح فحص"),
        ("withdraw", "سحب رصيد لحساب بنكي"),
    )
