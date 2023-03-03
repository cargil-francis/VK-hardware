from hardware.models import Address
from django import forms
import django
from django.utils.translation import gettext, gettext_lazy as _
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import CharField



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['locality', 'city', 'state']
        widgets = {'locality':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Popular Place like Restaurant, Religious Site, etc.'}), 'city':forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), 'state':forms.TextInput(attrs={'class':'form-control', 'placeholder':'State or Province'})}