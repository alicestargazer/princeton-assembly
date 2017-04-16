from django import forms
from .models import Problem

class AbsvalForm(forms.ModelForm):
    iInput = forms.CharField(label='iInput', max_length=100)
    class Meta:
        model = Problem
        fields = []

class PowerForm(forms.ModelForm):
    lBase = forms.CharField(label='lBase', max_length=100)
    lExp = forms.CharField(label='lExp', max_length=100)
    class Meta:
        model = Problem
        fields = []

class UppercaseForm(forms.ModelForm):
    cInput = forms.CharField(label='cInput', max_length=100)
    class Meta:
        model = Problem
        fields = []

class RectForm(forms.ModelForm):
    iLength = forms.CharField(label='iLength', max_length=100)
    iWidth = forms.CharField(label='iWidth', max_length=100)
    class Meta:
        model = Problem
        fields = []
