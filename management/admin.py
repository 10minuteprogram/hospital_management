from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(MedicalDepartment)
admin.site.register(MedicalDoctor)
admin.site.register(Specialist)