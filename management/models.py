from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class MedicalDepartment(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="dept_creared")
    update_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="dept_updated")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

class Specialist(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class MedicalDoctor(models.Model):
    department = models.ForeignKey(MedicalDepartment, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to='doctor/image', blank=True, null=True)
    specialist = models.ForeignKey(Specialist, on_delete=models.SET_NULL, blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="doctor_creared")
    update_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="doctor_updated")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name