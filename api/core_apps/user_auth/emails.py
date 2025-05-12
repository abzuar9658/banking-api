from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags    
from django.utils.translation import gettext_lazy as _
from loguru import logger

def send_otp_email(email, otp):
    subject = "OTP for Login"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context = {
        'otp': otp,
        'otp_expiration': settings.OTP_EXPIRATION.total_seconds() / 60,
        'site_name': settings.SITE_NAME,
    }
    html_content = render_to_string('emails/otp_email.html', context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, 'text/html')
    try:
        email.send()
        logger.info(f"OTP email sent to {email}")
    except Exception as e:
        logger.error(f"Error sending OTP email to {email}: {e}")
        raise e
        
def send_account_locked_email(self):
    subject = "Account Locked"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context = {
        'user': self.user,
        'lockout_duration': settings.LOCKOUT_DURATION.total_seconds() / 60,
        'site_name': settings.SITE_NAME,
    }
    html_content = render_to_string('emails/account_locked.html', context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, 'text/html')
    try:
        email.send()
        logger.info(f"Account locked email sent to {email}")
    except Exception as e:
        logger.error(f"Error sending account locked email to {email}: {e}")
        raise e
    