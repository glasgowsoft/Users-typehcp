from django                                 import forms
#from django.forms.widgets                   import CheckboxSelectMultiple
#from django.utils                           import timezone
#from django.contrib.auth.models             import User
from .models                                import Person
#from django.contrib.auth.forms              import SetPasswordForm, PasswordChangeForm


class UpdateMemberForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('username', 'display_name', 'status', 'authorname')

class UpdateContactForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('username', 'display_name', 'status', 'authorname')

class InsertMemberForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('username', 'display_name','password')

class InsertContactForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('username', 'display_name')

class PasswordForm(forms.Form):
    password = forms.CharField(label='New password', max_length=20)

class DisplaynameForm(forms.Form):
    display_name = forms.CharField(max_length=20)

class UserOptionsForm(forms.ModelForm):
     class Meta:
        model = Person
        #fields = ('display_name',)
        fields = ('username',)

class CurrentColoursForm(forms.Form):
  datecolor               = forms.CharField(max_length=20)
  detailcolor             = forms.CharField(max_length=20)
  attendeescolor          = forms.CharField(max_length=20)
  backgroundcolor         = forms.CharField(max_length=20)
