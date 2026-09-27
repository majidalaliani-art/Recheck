from config import session_value ,CLIENTKEY as KEY
import random
# import sys
# from pathlib import Path
# from django.shortcuts import render
# from django.apps import apps



def get_otp():
    return f"{random.randint(0, 10**KEY['OTP'] - 1):0{KEY['OTP']}d}"


# def setup_project_path(root_folder_name="Application"):
#     """
#     Set the project root folder in sys.path so all modules can be imported globally.

#     Args:
#         root_folder_name (str): The folder name to treat as project root.
#     """
#     home_dir = Path(__file__).resolve().parent
#     while home_dir.name != root_folder_name and home_dir.parent != home_dir:
#         home_dir = home_dir.parent

#     # Add the project root to sys.path if not already present
#     if str(home_dir) not in sys.path:
#         sys.path.insert(0, str(home_dir))

#     # Change working directory to the project root (optional)
#     os.chdir(home_dir)

# # ------------------------------
# # Usage: Call this first in urls.py
# # ------------------------------
# setup_project_path()




# import redis,random,re
# # Create your views here.
# # Connect to Redis once (can be reused)
# r = redis.Redis(host='localhost', port=6379, db=0)

# # This file handles session helpers
# # This function retrieves service-related data from the session


# ##########################################################################################################################################################################################################################################################################################################





# KEY = {

#     "LOGIN_PHONE": '/client/login.html',  # User login via phone number
#     'VERIFY_OTP' : 'login/verify.html', # WhatsApp or SMS verification message
#     'HOMEPAGE': 'services/homepage.html',  # Homepage of the site

#     'VILLA':'services/services/villa/home.html',
#     'BUYING' :'buying.html',




#     # 'APARTMENT':'',

#     'OTP_TTL':5 * 60, # 5 minutes in seconds
#     'OTP_RESEND_DELAY': 60 , # Waiting time before requesting a new OTP: 60 seconds

#     'MAX_ATTEMPTS'  :5 , # Maximum number of OTP requests allowed
#     'ATTEMPT_WINDOW' : 60, # Time window in seconds (1 minute)
#     'OTP': 4,  # Number of digits for the OTP
#     'OTP_CHECK': lambda otp_code: bool(re.fullmatch(r'\d{' + str(KEY['OTP']) + r'}', otp_code)), # Checks if OTP is numeric and has exact length defined in USER_KEY['OTP']
#     'OTP_FUNC': lambda: f"{random.randint(0, 10**KEY['OTP'] - 1):0{KEY['OTP']}d}", # Function to generate a 6-digit OTP on demand

#     'MAX_ATTEMPTS': 5,       # Maximum allowed OTP requests per IP
#     'WINDOW': 0 , # Time window in seconds to count attempts
# }



##########################################################################################################################################################################################################################################################################################################


# def some_view(request,page_name='user_login'):
#     # Store the current page path in the user's session

#     # Redirect the user to the login page (or any other page)
#     return render(request, page_name)



# def store_service(request, service_name, service_type, ttl=600):

#     """
#     Store service info in Redis using the user's IP as the key.
#     - r: Redis connection
#     - request: Django HttpRequest
#     - service_name: Name of the service (e.g., 'villa')
#     - service_type: Type of the service (e.g., 'service_basic')
#     - ttl: Optional expiration time in seconds
#     """
#     # Get client IP (handles proxies if behind them)
#     ip = request.META.get('HTTP_X_FORWARDED_FOR')
#     if ip:
#         ip = ip.split(',')[0].strip()
#     else:
#         ip = request.META.get('REMOTE_ADDR', 'unknown')

#     key = f"service:{ip}"

#     r.hset(key, mapping={
#         "service_name": service_name,
#         "service_type": service_type
#     })

#     if ttl:
#         r.expire(key, ttl)




# def get_service(request):
#     """
#     Retrieve service info from Redis using the user's IP.
#     Returns a dict: {'service_name': ..., 'service_type': ...} or empty dict if not found.
#     """
#     # Get client IP
#     ip = request.META.get('HTTP_X_FORWARDED_FOR')
#     if ip:
#         ip = ip.split(',')[0].strip()
#     else:
#         ip = request.META.get('REMOTE_ADDR', 'unknown')

#     key = f"service:{ip}"

#     data = r.hgetall(key)

#     # Convert bytes to string (Redis returns bytes)
#     if data:
#         return {k.decode(): v.decode() for k, v in data.items()}
#     return {}



# import re
# def clean_text(text):
#     # Replace dangerous characters with empty string
#     # Allow Arabic, English, numbers 0-9, spaces, and . , ? ! : - only
#     if not text:
#         return ""
#     allowed_pattern = r"[^a-zA-Z0-9\u0600-\u06FF\s\.\,\?\!\:\-]"
#     cleaned = re.sub(allowed_pattern, "", text)
#     return cleaned









# def validate_coordinates(lat, lng):
#     """
#     Validate latitude and longitude numbers.
#     Returns True if valid, False otherwise.
#     """
#     try:
#         lat = float(lat)
#         lng = float(lng)
#     except (ValueError, TypeError):
#         return False

#     # Latitude must be between -90 and 90
#     if not (-90 <= lat <= 90):
#         return False

#     # Longitude must be between -180 and 180
#     if not (-180 <= lng <= 180):
#         return False

#     return True












# def check_ip_block(request):
#     """
#     Check if the client's IP should be blocked due to too many OTP requests.
#     Returns True if blocked, False otherwise.
#     """
#     # Only count POST requests
#     if request.method != "POST":
#         print (False)
#         return False

#     # Get client IP address
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')

#     # Redis key to track attempts per IP
#     attempt_key = f"otp_attempts:{ip}"

#     # Increment the attempt counter
#     attempts = r.incr(attempt_key)
#     if attempts == 5:
#         # First attempt, set key expiration for the time window
#         r.expire(attempt_key, KEY['WINDOW'])

#     # Check if the attempts exceed the maximum allowed
#     if attempts > KEY['MAX_ATTEMPTS']:
#         return True  # IP is blocked
#     return False    # IP is allowed
