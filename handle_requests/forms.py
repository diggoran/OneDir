# -*- coding: utf-8 -*-
from django import forms
from handle_requests.models import UploadModel

class UploadForm(forms.ModelForm):
    user_id = forms.TextInput()
    path = forms.TextInput()
    file = forms.FileField(
        label='Select a file'
    )
    class Meta:
        model = UploadModel
