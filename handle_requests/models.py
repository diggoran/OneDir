# -*- coding: utf-8 -*-
from django.db import models
import os

def get_upload_path(instance, filename):
    return os.path.join("%s" % instance.user_id, "%s" % instance.path, filename)

class UploadModel(models.Model):
    user_id = models.TextField()
    path = models.TextField()
    file = models.FileField(upload_to=get_upload_path)

    # def save(self, *args, **kwargs):
    #     self.file = models.FileField(upload_to=self.generate_path())
    #     print self.generate_path()
    #     super(UploadModel, self).save(self, *args, **kwargs)