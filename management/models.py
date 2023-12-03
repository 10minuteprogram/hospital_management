from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.FileField(upload_to='user/profile/images', blank=True, null=True)
    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_email_active = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

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

    hospital = models.CharField(max_length=120, blank=True, null=True)

    slug = models.SlugField(unique=True, blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="doctor_creared")
    update_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="doctor_updated")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            i = 1
            while MedicalDoctor.objects.filter(slug=slug).exists():
                temp_slug = slugify(self.name)
                slug = f"{temp_slug}-{i}"
                i = i + 1
            
            self.slug = slug
        super(MedicalDoctor, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('name', 'department')

    def __str__(self):
        return self.name
    
    