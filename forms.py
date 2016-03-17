from django                                 import forms
from django.forms.widgets                   import CheckboxSelectMultiple
from django.utils                           import timezone
from django.contrib.auth.models             import User
from .models                                import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('username', 'display_name', 'email', 'password', 'status', 'date_joined', 'landline', 'mobile', 'postal_address', 'notes')

