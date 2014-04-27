from django.db import models

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=128)
    path = models.CharField(max_length=128)
    time_stamp = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(default=-1)
    size = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name

class Modification(models.Model):
    file_id = models.IntegerField(default=-1)
    user_id = models.IntegerField(default=-1)
    time_stamp = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.pk)

class Connection(models.Model):
    user_id = models.IntegerField(default=-1)
    time_stamp = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.pk)

class Access(models.Model):
    user_id = models.IntegerField(default=-1)
    file_id = models.IntegerField(default=-1)
    def __unicode__(self):
        return str(self.pk)

#class UploadModel(models.Model):
#	file = models.FileField(upload_to='uploads/$Y/%m/%d/%H/%M/%S/')
