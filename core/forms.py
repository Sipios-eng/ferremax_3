from django import forms
from .models import *

class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=2,max_length=15)
    name = forms.CharField(min_length=3,max_length=15)
    last_name = forms.CharField(min_length=3,max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    email2 = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')
        email2 = cleaned_data.get('email2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden!')
        if email and email2 and email != email2:
            raise forms.ValidationError('Los correos no coinciden!')