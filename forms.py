from django                                 import forms
from django.forms.widgets                   import CheckboxSelectMultiple
from django.utils                           import timezone
from django.contrib.auth.models             import User
from .models                                import Person
from django.contrib.auth.forms              import SetPasswordForm, PasswordChangeForm


class UpdatePersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('username', 'display_name', 'password', 'status')
class InsertPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('username', 'display_name', 'password')
class PasswordForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('password',)
class DisplaynameForm(forms.Form):
    display_name = forms.CharField(max_length=20)


