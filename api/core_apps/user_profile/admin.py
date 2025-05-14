from cloudinary.forms import CloudinaryFileField
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.contrib import admin

from .models import Profile, NextOfKin

class ProfileAdminForm(forms.ModelForm):
    photo = CloudinaryFileField(
        options={
            'crop': 'thumb',
            'width': 200,
            'height': 200,
            'folder': 'profile_photos',
            'transformation': [
                {'crop': 'thumb', 'width': 150, 'height': 150}
            ],
        },
        required=False,
    )
    
    class Meta:
        model = Profile
        fields = '__all__'
        
class NextOfKinInline(admin.TabularInline):
    model = NextOfKin
    extra = 1
    fields = ['first_name', 'last_name', 'relationship', 'phone_number', 'email_address']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    inlines = [NextOfKinInline]
    list_display = ['user', 'title', 'gender', 'date_of_birth', 'martial_status', 'address']
    list_filter = ['gender', 'martial_status', 'employment_status']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'address']
    readonly_fields = ['user']
    fieldsets = (
        (None, {'fields': ('user', 'photo')}),
        (_('Personal Information'), {
            'fields': ('title', 'gender', 'date_of_birth', 'martial_status', 'nationality')
        }),
        (_('Identification'), {
            'fields': ('identification_means', 'identification_number', 
                      'identification_issue_date', 'identification_expiry_date')
        }),
        (_('Employment'), {
            'fields': ('employment_status', 'employment_type', 'occupation', 
                      'employer_name', 'annual_income', 'date_of_employment',
                      'employer_address', 'employer_city')
        }),
        (_('Address & Contact'), {
            'fields': ('address', 'country_of_birth', 'country_of_residence')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['user']
        return self.readonly_fields
    
@admin.register(NextOfKin)
class NextOfKinAdmin(admin.ModelAdmin):
    list_display = ['profile', 'first_name', 'last_name', 'relationship', 'phone_number', 'email_address']
    list_filter = ['relationship', 'is_primary']
    search_fields = ['profile__user__email', 'first_name', 'last_name', 'email_address']
    
    
    
    
    
    
    