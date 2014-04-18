# -*- coding: utf-8 -*-
from django import forms
from handle_requests.models import UploadModel

class UploadForm(forms.ModelForm):
    file = forms.FileField(
        label='Select a file'
    )
    class Meta:
        model = UploadModel
