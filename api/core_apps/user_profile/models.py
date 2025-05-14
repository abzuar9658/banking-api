from typing import Any
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core_apps.common.models import TimeStampModel

User = get_user_model()

class Profile(TimeStampModel):
    class Salutation(models.TextChoices):
        MR = ('mr', _('Mr'),)
        MRS = ('mrs', _('Mrs'),)
        MS = ('ms', _('Ms'),)
        DR = ('dr', _('Dr'),)
    
    class Gender(models.TextChoices):
        MALE = ('male', _('Male'),)
        FEMALE = ('female', _('Female'),)
        OTHER = ('other', _('Other'),)
    
    class MaritalStatus(models.TextChoices):
        SINGLE = ('single', _('Single'),)
        MARRIED = ('married', _('Married'),)
        DIVORCED = ('divorced', _('Divorced'),)
        WIDOWED = ('widowed', _('Widowed'),)
        SEPARATED = ('separated', _('Separated'),)
        UNKNOWN = ('unknown', _('Unknown'),)

    class IdentificationMeans(models.TextChoices):
        PASSPORT = ('passport', _('Passport'),)
        NATIONAL_ID = ('national_id', _('National ID'),)
        DRIVERS_LICENSE = ('drivers_license', _('Drivers License'),)
        VOTERS_ID = ('voters_id', _('Voters ID'),)
        OTHER = ('other', _('Other'),)
    
    class EmploymentStatus(models.TextChoices):
        EMPLOYED = ('employed', _('Employed'),)
        SELF_EMPLOYED = ('self_employed', _('Self Employed'),)
        UNEMPLOYED = ('unemployed', _('Unemployed'),)
        RETIRED = ('retired', _('Retired'),)
        STUDENT = ('student', _('Student'),)
        OTHER = ('other', _('Other'),)
    
    class EmploymentType(models.TextChoices):
        FULL_TIME = ('full_time', _('Full Time'),)
        PART_TIME = ('part_time', _('Part Time'),)
        CONTRACT = ('contract', _('Contract'),)
        VOLUNTEER = ('volunteer', _('Volunteer'),)
        OTHER = ('other', _('Other'),)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(
        max_length=3,
        choices=Salutation.choices,
        default=Salutation.MR,
        verbose_name=_('Title'),
        help_text=_('The title of the user'),
    )
    gender = models.CharField(
        max_length=6,
        choices=Gender.choices,
        default=Gender.MALE,
        verbose_name=_('Gender'),
        help_text=_('The gender of the user'),
    )
    date_of_birth = models.DateField(
        verbose_name=_('Date of Birth'),
        help_text=_('The date of birth of the user'),
        validators=[MinValueValidator(settings.DEFAULT_BIRTH_DATE)],
        blank=True,
        null=True,
    )
    martial_status = models.CharField(
        max_length=10,
        choices=MaritalStatus.choices,
        default=MaritalStatus.SINGLE,
        verbose_name=_('Martial Status'),
        help_text=_('The martial status of the user'),
    )
    country_of_birth = CountryField(
        verbose_name=_('Country of Birth'),
        help_text=_('The country of birth of the user'),
        default=settings.DEFAULT_COUNTRY,
        blank=True,
        null=True,
    )
    country_of_residence = CountryField(
        verbose_name=_('Country of Residence'),
        help_text=_('The country of residence of the user'),
        default=settings.DEFAULT_COUNTRY,
        blank=True,
        null=True,
    )
    identification_means = models.CharField(
        max_length=16,
        choices=IdentificationMeans.choices,
        default=IdentificationMeans.NATIONAL_ID,
        verbose_name=_('Identification Means'),
        help_text=_('The means of identification of the user'),
    )
    identification_number = models.CharField(
        max_length=12,
        verbose_name=_('Identification Number'),
        help_text=_('The identification number of the user'),
        blank=True,
        null=True,
    )
    identification_issue_date = models.DateField(
        verbose_name=_('Identification Issue Date'),
        help_text=_('The issue date of the identification of the user'),
        blank=True,
        null=True,
    )
    identification_expiry_date = models.DateField(
        verbose_name=_('Identification Expiry Date'),
        help_text=_('The expiry date of the identification of the user'),
        blank=True,
        null=True,
    )
    employment_status = models.CharField(
        max_length=15,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.EMPLOYED,
        verbose_name=_('Employment Status'),
        help_text=_('The employment status of the user'),
    )
    employment_type = models.CharField(
        max_length=12,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL_TIME,
        verbose_name=_('Employment Type'),
        help_text=_('The type of employment of the user'),  
    )
    passport_number = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        verbose_name=_('Passport Number'),
        help_text=_('The passport number of the user'),
    )
    nationality = CountryField(
        verbose_name=_('Nationality'),
        help_text=_('The nationality of the user'),
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=12,
        verbose_name=_('Address'),
        help_text=_('The address of the user'),
        blank=True,
        null=True,
    )
    occupation = models.CharField(
        max_length=15,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.EMPLOYED,
        verbose_name=_('Occupation'),
        help_text=_('The occupation of the user'),
    )
    employer_name = models.CharField(
        max_length=12,
        verbose_name=_('Employer Name'),
        help_text=_('The name of the employer of the user'),
        blank=True,
        null=True,
    )
    annual_income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Annual Income'),
        help_text=_('The annual income of the user'),
        blank=True,
        null=True,
    )
    date_of_employment = models.DateField(
        verbose_name=_('Date of Employment'),
        help_text=_('The date of employment of the user'),
        blank=True,
        null=True,
    )
    employer_address = models.CharField(
        max_length=12,
        verbose_name=_('Employer Address'),
        help_text=_('The address of the employer of the user'),
        blank=True,
        null=True,
    )
    employer_city = models.CharField(
        max_length=12,
        verbose_name=_('Employer City'),
        help_text=_('The city of the employer of the user'),
        blank=True,
        null=True,
    )
    photo = CloudinaryField(
        blank=True,
        null=True,
        verbose_name=_('Photo'),
        help_text=_('The photo of the user'),
    )
    photo_url = models.URLField(
        verbose_name=_('Photo URL'),
        help_text=_('The URL of the photo of the user'),
        blank=True,
        null=True,
    )
    id_photo = CloudinaryField(
        blank=True,
        null=True,
        verbose_name=_('ID Photo'),
        help_text=_('The ID photo of the user'),
    )
    id_photo_url = models.URLField(
        verbose_name=_('ID Photo URL'),
        help_text=_('The URL of the ID photo of the user'),
        blank=True,
        null=True,
    )
    signature_photo = CloudinaryField(
        blank=True,
        null=True,
        verbose_name=_('Signature Photo'),
        help_text=_('The signature photo of the user'),
    )
    signature_photo_url = models.URLField(
        verbose_name=_('Signature Photo URL'),
        help_text=_('The URL of the signature photo of the user'),
        blank=True,
        null=True,
    )
    
    def clean(self):
        super().clean()
        if self.identification_issue_date and self.identification_expiry_date:
            if self.identification_issue_date > self.identification_expiry_date:
                raise ValidationError(_('The issue date of the identification must be before the expiry date'))
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    
    def is_complete_with_next_of_kin(self):
        required_fields = [
            self.title,
            self.gender,
            self.date_of_birth,
            self.martial_status,
            self.country_of_birth,
            self.country_of_residence,
            self.identification_means,
            self.identification_number,
            self.identification_issue_date,
            self.identification_expiry_date,
            self.employment_status,
            self.employment_type,
            self.passport_number,
            self.nationality,
            self.address,
            self.occupation,
            self.employer_name,
            self.annual_income,
        ]
        return all(required_fields) and self.next_of_kin.exists()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class NextOfKin(TimeStampModel):
    class Salutation(models.TextChoices):
        MR = ('mr', _('Mr'),)
        MRS = ('mrs', _('Mrs'),)
        MS = ('ms', _('Ms'),)
        DR = ('dr', _('Dr'),)
    
    class Gender(models.TextChoices):
        MALE = ('male', _('Male'),)
        FEMALE = ('female', _('Female'),)
        OTHER = ('other', _('Other'),)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='next_of_kin')
    title = models.CharField(
        max_length=3,
        choices=Salutation.choices,
        default=Salutation.MR,
        verbose_name=_('Title'),
        help_text=_('The title of the next of kin'),
    )
    first_name = models.CharField(
        max_length=12, 
        verbose_name=_('First Name'), 
        help_text=_('The first name of the next of kin'),
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=12, 
        verbose_name=_('Last Name'), 
        help_text=_('The last name of the next of kin'),
        blank=True,
        null=True,
    )
    other_names = models.CharField(
        max_length=12, 
        verbose_name=_('Other Names'), 
        help_text=_('The other names of the next of kin'),
        blank=True,
        null=True,
    )
    gender = models.CharField(
        max_length=6, 
        choices=Gender.choices, 
        default=Gender.MALE, 
        verbose_name=_('Gender'), 
        help_text=_('The gender of the next of kin')
    )
    date_of_birth = models.DateField(
        verbose_name=_('Date of Birth'), 
        help_text=_('The date of birth of the next of kin'),
        blank=True,
        null=True,
    )
    relationship = models.CharField(
        max_length=12, 
        verbose_name=_('Relationship'), 
        help_text=_('The relationship of the next of kin'),
        blank=True,
        null=True,
    )
    email_address = models.EmailField(
        verbose_name=_('Email Address'), 
        help_text=_('The email address of the next of kin'),
        blank=True,
        null=True,
    )
    phone_number = PhoneNumberField(
        verbose_name=_('Phone Number'), 
        help_text=_('The phone number of the next of kin'),
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=12, 
        verbose_name=_('Address'), 
        help_text=_('The address of the next of kin'),
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=12, 
        verbose_name=_('City'), 
        help_text=_('The city of the next of kin'),
        blank=True,
        null=True,
    )
    country = CountryField(
        verbose_name=_('Country'), 
        help_text=_('The country of the next of kin'),
        blank=True,
        null=True,
    )
    is_primary = models.BooleanField(default=False, verbose_name=_('Is Primary'), help_text=_('Whether the next of kin is the primary next of kin'))
    
    def clean(self):
        super().clean()
        if self.is_primary and self.profile.next_of_kin.filter(is_primary=True).exclude(id=self.id).exists():
            raise ValidationError(_('Only one primary next of kin is allowed'))
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} - Next of Kin for {self.profile.user.first_name} {self.profile.user.last_name}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'is_primary'],
                condition=models.Q(is_primary=True),
                name='unique_primary_next_of_kin',
            ),
        ]
    
