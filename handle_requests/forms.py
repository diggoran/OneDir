# -*- coding: utf-8 -*-
from django import forms
from handle_requests.models import UploadModel

class UploadForm(forms.ModelForm):
    username = forms.TextInput()
    path = forms.TextInput()
    file_name = forms.TextInput()
    size = forms.IntegerField()
    password = forms.TextInput()
    file = forms.FileField(
        label='Select a file'
    )
    class Meta:
        model = UploadModel
