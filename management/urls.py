from django.urls import path
from .views import *


urlpatterns = [
    path('',home, name='home'),
    path('manage-doctor/', manage_doctor, name='manage_doctor'),
    path('new_department/', new_department, name='new_department'),
    path('new_specialist/', new_specialist, name="new_specialist"),
    path('new_doctor/', new_doctor, name="new_doctor"),
]
