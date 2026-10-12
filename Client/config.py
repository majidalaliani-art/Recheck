import random
from .constants import PATH as KEY

def get_otp():
    return f"{random.randint(0, 10**KEY['OTP'] - 1):0{KEY['OTP']}d}"
