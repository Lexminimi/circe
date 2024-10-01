from django.contrib import admin

# Register your models here.
from .models import Students, ClassGroups, Attendance, Presence

admin.site.register(Students)
admin.site.register(ClassGroups)
admin.site.register(Attendance)
admin.site.register(Presence)