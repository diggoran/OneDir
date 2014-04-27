from django.contrib import admin
from onedir.models import File, Connection, Modification, Access

admin.site.register(File)
admin.site.register(Connection)
admin.site.register(Modification)
admin.site.register(Access)
