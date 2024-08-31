from django.contrib import admin

# Register your models here.
from .models import Students, ClassGroups, Classes

admin.site.register(Students)
admin.site.register(ClassGroups)
admin.site.register(Classes)