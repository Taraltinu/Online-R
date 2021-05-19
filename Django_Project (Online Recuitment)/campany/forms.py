from django import forms

# from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import MyUser

class UserCreation_Form(UserCreationForm):
	class Meta(UserCreationForm):
		model = MyUser
		fields =("email",)



class UserChange_form(UserChangeForm):
	class Meta(UserChangeForm):
		model = MyUser
		fields =("email",)


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control', 'id':'password','placeholder': 'New Password'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control',"id":"password2",'placeholder': 'New Password Confirm'}))

# send email forms
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class':'form-control','placeholder': 'Enter Your Registered Email*'}))  
