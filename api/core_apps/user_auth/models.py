import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from .emails import send_account_locked_email
from .managers import UserManager

class User(AbstractBaseUser):
    class SecurityQuestions(models.TextChoices):
        FAVORITE_COLOR = 'favorite_color', _('Favorite Color')
        FIRST_PET = 'first_pet', _('First Pet')
        MOTHER_MAIDEN_NAME = 'mother_maiden_name', _('Mother\'s Maiden Name')
        BIRTH_CITY = 'birth_city', _('Birth City')
        CHILDHOOD_FRIEND = 'childhood_friend', _('Childhood Friend')
        
    class AccountStatus(models.TextChoices):
        ACTIVE = 'active', _('Active')
        LOCKED = 'locked', _('Locked')
        INACTIVE = 'inactive', _('Inactive')
        
    class RoleChoices(models.TextChoices):
        CUSTOMER = 'customer', _('Customer')
        ACCOUNT_EXECUTIVE = 'account_executive', _('Account Executive')
        CUSTOMER_SERVICE_REPRESENTATIVE = 'customer_service_representative', _('Customer Service Representative')
        BANK_TELLER = 'bank_teller', _('Bank Teller')
        BANK_MANAGER = 'bank_manager', _('Bank Manager')
        BANK_ADMINISTRATOR = 'bank_administrator', _('Bank Administrator')
        BANK_AUDITOR = 'bank_auditor', _('Bank Auditor')
        BANK_TECHNICIAN = 'bank_technician', _('Bank Technician')
        BANK_SECURITY_GUARD = 'bank_security_guard', _('Bank Security Guard')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(_('Username'), max_length=50, unique=True)
    security_question = models.CharField(_('Security Question'), max_length=50, choices=SecurityQuestions.choices)
    security_answer = models.CharField(_('Security Answer'), max_length=100)
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(_('First Name'), max_length=30)
    middle_name = models.CharField(_('Middle Name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=30)
    id_no = models.PositiveBigIntegerField(_('ID Number'), unique=True)
    account_status = models.CharField(_('Account Status'), max_length=50, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)
    role = models.CharField(_('Role'), max_length=50, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER)
    failed_login_attempts = models.PositiveSmallIntegerField(_('Failed Login Attempts'), default=0)
    last_failed_login = models.DateTimeField(_('Last Failed Login'), null=True, blank=True)
    otp = models.CharField(_('OTP'), max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(_('OTP Expiry'), null=True, blank=True)
    is_superuser = models.BooleanField(_('Is Superuser'), default=False)
    is_staff = models.BooleanField(_('Is Staff'), default=False)
    date_joined = models.DateTimeField(_('Date Joined'), default=timezone.now)
    created_at = models.DateTimeField(_('Created At'), default=timezone.now)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'id_no', 'security_question', 'security_answer']
        
    def set_otp(self, otp: str) -> None:
        self.otp = otp
        self.otp_expiry = timezone.now() + settings.OTP_EXPIRY_TIME
        self.save(update_fields=['otp', 'otp_expiry'])
    
    def verify_otp(self, otp: str) -> bool:
        if self.otp == otp and self.otp_expiry > timezone.now():
            self.clear_otp()
            return True
        return False

    def clear_otp(self) -> None:
        self.otp = None
        self.otp_expiry = None
        self.save(update_fields=['otp', 'otp_expiry'])
    
    def handle_failed_login(self) -> None:
        self.increment_failed_login_attempts()
        if self.is_account_locked():
            self.lock_account()
            send_account_locked_email(self)

    def increment_failed_login_attempts(self) -> None:
        self.failed_login_attempts += 1
        self.last_failed_login = timezone.now()
        self.save(update_fields=['failed_login_attempts', 'last_failed_login'])
    
    def reset_failed_login_attempts(self) -> None:
        self.failed_login_attempts = 0
        self.last_failed_login = None
        self.save(update_fields=['failed_login_attempts', 'last_failed_login'])
    
    def is_account_locked(self) -> bool:
        return self.failed_login_attempts >= settings.MAX_FAILED_LOGIN_ATTEMPTS
    
    def lock_account(self) -> None:
        self.account_status = self.AccountStatus.LOCKED
        self.save(update_fields=['account_status'])
        
    def unlock_account(self) -> None:
        self.account_status = self.AccountStatus.ACTIVE
        self.save(update_fields=['account_status'])
        
    @property
    def is_locked_out(self) -> bool:
        if self.account_status == self.AccountStatus.LOCKED:
            if self.last_failed_login + settings.LOCKOUT_DURATION < timezone.now():
                self.unlock_account()
                return False
            return True
        return False
    
    @property
    def full_name(self) -> str:
        full_name = f"{self.first_name} {self.middle_name} {self.last_name}"
        return full_name.title().strip()
    
    class Meta:
        ordering = ['-date_joined', '-created_at']
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def has_role(self, role: str) -> bool:
        return hasattr(self, 'role') and self.role == role

    def has_permission(self, permission: str) -> bool:
        return hasattr(self, 'role') and self.role == permission
    
    def __str__(self) -> str:
        return f"{self.full_name} - {self.get_role_display()}"
    
    