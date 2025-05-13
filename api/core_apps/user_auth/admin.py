from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from .forms import UserChangeForm, UserCreationForm

@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'role', 'account_status')
    list_filter = ('email', 'is_superuser', 'role', 'account_status')
    search_fields = ('email', 'first_name', 'last_name', 'id_no')
    ordering = ('email',)
    filter_horizontal = ()
    
    fieldsets = (
        (_('Login Credentials'), {
            'fields': ('username', 'email', 'password')
        }),
        (_('Personal Info'), {
            'fields': ('first_name', 'middle_name', 'last_name', 'id_no', 'security_question', 'security_answer')
        }),
        (_('Permissions'), {
            'fields': ('is_superuser', 'role')
        }),
        (_('Account Status'), {
            'fields': ('account_status', 'failed_login_attempts', 'last_failed_login')
        }),
        (_('Security'), {
            'fields': ('otp', 'otp_expiry')
        }),
        (_('Important Dates'), {
            'fields': ('last_login',)
        })
    )
    
    add_fieldsets = (
        (_('Login Credentials'), {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
        (_('Personal Info'), {
            'fields': ('first_name', 'middle_name', 'last_name', 'id_no', 'security_question', 'security_answer')
        }),
        (_('Role'), {
            'fields': ('role',)
        })
    )