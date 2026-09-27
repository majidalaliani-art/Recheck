from django.core.cache import cache

from django.apps import apps

import random


##########################################################################################################################################################################################################################################################################################################

from django.apps import apps
import random
def generate_otp(length=4):
    return "".join([str(random.randint(0, 9)) for _ in range(length)])

def get_client_latest_row(request, app_name, model_name):
    """
    Retrieves the latest record for the logged-in user from a specific model.
    """
    # 1. Get the identifier from the session
    user_phone = session_value(request, key='user_id')

    # If there's no user in session, return None immediately
    if not user_phone:
        return None

    try:
        # 2. Get the model dynamically
        Model = apps.get_model(app_name, model_name)

        # 3. Filter by phone and get the most recent row
        # This ensures you only get rows belonging to THIS person
        return Model.objects.filter(phone=user_phone).order_by('-id').first()

    except LookupError:
        # Return None if app or model names are incorrect
        return None


def session_value(request, key, value=None, default=None, check=None, delete=False):
    """
    - Store `value` in session if given.
    - If `delete=True` → remove the key from session (logout/delete user).
    - If `check` is given → return True if session value equals it, else False.
    - Otherwise → return the session value or default.
    """

    # Delete key from session if requested
    if delete:
        return request.session.pop(key, None) # Returns the value if existed, else None

    # Store the value if provided
    if value is not None:
        request.session[key] = value

    # Check if we need to compare
    if check is not None:
        return request.session.get(key, None) == check

    # Return the value or default
    if default is not None:
        request.session[key] = default
        return request.session.get(key, default)

    # If no value or check, just return the value or False
    if key in request.session:
        return request.session[key]  # Return stored value
    else:
        return None


def cache_value(request, key=None, value=None, default=None, check_key=None, check_value=None, delete=False, timeout=600):
    """
    Handles caching with support for dictionary merging and single value overwriting.
    """
    # 1. Resolve the cache key
    if key is None:
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')
        key = f"ip_{ip}"

    # 2. Handle deletion
    if delete:
        return cache.delete(key)

    # Fetch existing data for potential merging
    stored_data = cache.get(key)

    # 3. Handle Storing (Merge if both are dicts, otherwise Overwrite)
    if value is not None:
        if isinstance(value, dict) and isinstance(stored_data, dict):
            # If both are dictionaries, merge them
            stored_data.update(value)
            cache.set(key, stored_data, timeout)
            return stored_data
        else:
            # If new value is a single value (string/int) or cache was empty/not a dict:
            # Direct override (will delete previous dictionary if value is a string)
            cache.set(key, value, timeout)
            return value

    # 4. Handle Flexible Comparison
    if check_value is not None:
        if check_key is not None and isinstance(stored_data, dict):
            # Compare specific key inside a dictionary
            return str(stored_data.get(check_key)) == str(check_value)

        # Compare direct single value
        return str(stored_data) == str(check_value)

    # 5. Handle Retrieval
    return stored_data if stored_data is not None else (default if default is not None else {})

CLIENTKEY = {
    "LOGIN": 'Client/login.html',  # User login via phone number

    'HOMEPAGE': 'Client/homepage.html',  # Homepage of the site
    'VILLA':'Client/villa.html',
    'BUYING' :'Client/buying.html',
    # 'APARTMENT':'',
    'OTP_TTL':5 * 60, # 5 minutes in seconds
    'OTP_RESEND_DELAY': 60 , # Waiting time before requesting a new OTP: 60 seconds
    'MAX_ATTEMPTS'  :5 , # Maximum number of OTP requests allowed
    'ATTEMPT_WINDOW' : 60, # Time window in seconds (1 minute)
    'OTP': 4,  # Number of digits for the OTP
    'MAX_ATTEMPTS': 5,       # Maximum allowed OTP requests per IP
    'WINDOW': 0 , # Time window in seconds to count attempts
}


VISITS_ENGINEERKEY_PATH = {
    'START_VISIT' : 'Engineer/Visits/start_visit.html',
}


##########################################################################################################################################################################################################################################################################################################
class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.pop('required', None)
            if self.errors.get(name):
                field.widget.attrs["class"] = (
                    'error form-control glass-input form-label form-label write flatpickr-input'
                )
            else:
                field.widget.attrs["class"] = 'form-control glass-input form-label text-center'


import random


def generate_number(model, field_name="pk"):
    while True:
        length = random.randint(5, 8)
        new_id = "".join(random.choices("0123456789", k=length))

        exists = model.objects.filter(**{field_name: new_id}).exists()

        if not exists:
            return new_id
