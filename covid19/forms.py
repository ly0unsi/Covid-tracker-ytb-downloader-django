from django.forms import ModelForm
from .models import *
from django import forms


class emailForm(ModelForm):

    class Meta:
        model = Email
        fields = '__all__'
