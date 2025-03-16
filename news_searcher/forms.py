from django import forms
from .models import *
import os
from django.core.exceptions import ValidationError









class KeywordRecordForm(forms.ModelForm):
    class Meta:
        model = KeywordRecord
        fields = ['keyword', 'correlation_words', 'description']

        # chnge the field class as form-control
        widgets = {
            'keyword': forms.TextInput(attrs={'class': 'form-control'}),
            'correlation_words': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class MailGroupForm(forms.ModelForm):
    class Meta:
        model = MailGroup
        fields = ['name', 'level']

        # chnge the field class as form-control
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mails': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'level': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': '1', 'max': '3', 'value': '3'}),
        }



class ExclusionSiteRecordForm(forms.ModelForm):
    class Meta:
        model = ExclusionSiteRecord
        fields = ['site']

        # chnge the field class as form-control
        widgets = {
            'site': forms.TextInput(attrs={'class': 'form-control'}),
        }