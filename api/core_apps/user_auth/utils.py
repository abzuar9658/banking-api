import random
import string
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

def generate_otp(length=6) -> str:
    return ''.join(random.choices(string.digits, k=length))