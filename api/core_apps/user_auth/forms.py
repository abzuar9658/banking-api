from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User

class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'id_no', 'security_question', 'security_answer', 'is_superuser', 'is_staff', 'role')
        
    def clean_email(self) -> str:
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('This email address is already in use.'))
        return email
    
    def clean_id_no(self) -> str:
        id_no = self.cleaned_data.get('id_no')
        if User.objects.filter(id_no=id_no).exists():
            raise ValidationError(_('This ID number is already in use.'))
        return id_no
    
    def clean_security_answer(self) -> str:
        security_answer = self.cleaned_data.get('security_answer')
        if len(security_answer) < 3:
            raise ValidationError(_('Security answer must be at least 3 characters long.'))
        return security_answer
    
    def clean(self):
        cleaned_data = super().clean()
        is_superuser = cleaned_data.get('is_superuser')
        security_question = cleaned_data.get('security_question')
        security_answer = cleaned_data.get('security_answer')
        
        if is_superuser:
            cleaned_data['is_staff'] = True
        elif not security_question or not security_answer:
            self.add_error('security_question', _('Security question and answer are required.'))
        
        return cleaned_data

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user        
    
class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'id_no', 'security_question', 'security_answer', 'is_superuser', 'is_staff', 'role')
    
    def clean_email(self) -> str:
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError(_('This email address is already in use.'))
        return email

    def clean_id_no(self) -> str:
        id_no = self.cleaned_data.get('id_no')
        if User.objects.exclude(pk=self.instance.pk).filter(id_no=id_no).exists():
            raise ValidationError(_('This ID number is already in use.'))
        return id_no

    def clean_security_answer(self) -> str:
        security_answer = self.cleaned_data.get('security_answer')
        if len(security_answer) < 3:
            raise ValidationError(_('Security answer must be at least 3 characters long.'))
        return security_answer
    
    def clean(self):
        cleaned_data = super().clean()
        is_superuser = cleaned_data.get('is_superuser')
        security_question = cleaned_data.get('security_question')
        security_answer = cleaned_data.get('security_answer')
        
        if is_superuser:
            cleaned_data['is_staff'] = True
        elif not security_question or not security_answer:
            self.add_error('security_question', _('Security question and answer are required.'))
                
        return cleaned_data
    
    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        if commit:
            user.save()
        return user