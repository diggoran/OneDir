# -*- coding: utf-8 -*-
from django.db import models

class UploadModel(models.Model):
    user_id = models.TextField()
    path = models.TextField()
    file = models.FileField(upload_to='uploads/')

    def generate_path(self):
        return str(self.user_id + '/' + self.path + '/')

    def save(self, *args, **kwargs):
        self.file = models.FileField(upload_to=self.generate_path())
        print self.generate_path()
        super(UploadModel, self).save(self, *args, **kwargs)