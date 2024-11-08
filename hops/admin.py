from django.contrib import admin

# Register your models here.
from .models import Students, ClassGroups, AttendanceSheet, Presence, AttendanceRecord

admin.site.register(Students)
admin.site.register(ClassGroups)
admin.site.register(AttendanceSheet)
admin.site.register(Presence)
admin.site.register(AttendanceRecord)