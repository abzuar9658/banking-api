import random
import string
from os import getenv
from typing import Optional, Any

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
    
def generate_username(email: str) -> str:
    bank_name = getenv("BANK_NAME")
    words = bank_name.split()
    prefix = ''.join([word[0].lower() for word in words]).upper()
    remaining_length = 12 - len(prefix) - 1
    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=remaining_length))
    return f"{prefix}{random_suffix}"

def validate_email_address(email: str) -> str:
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError(_('Enter a valid email address'))
    return email

class UserManager(DjangoUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('An email address is required'))
        
        if not password:
            raise ValueError(_('A password is required'))
        
        email = self.normalize_email(email)
        email = validate_email_address(email)
        username = generate_username(email)
        
        # Ensure is_staff is True for superusers
        if extra_fields.get('is_superuser'):
            extra_fields['is_staff'] = True
            
        user = self.model(email=email, username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email: str, password: Optional[str] = None, **extra_fields) -> Any:
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email: str, password: Optional[str] = None, **extra_fields) -> Any:
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned to is_superuser=True.'))
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True.'))
        
        return self._create_user(email, password, **extra_fields)
