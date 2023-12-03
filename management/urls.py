from django.urls import path
from .views import *


urlpatterns = [
    path('',home, name='home'),
    path('manage-doctor/', manage_doctor, name='manage_doctor'),
    path('new_department/', new_department, name='new_department'),
    path('new_specialist/', new_specialist, name="new_specialist"),
    path('new_doctor/', new_doctor, name="new_doctor"),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('sign-in/', signin, name='sign-in'),
    path('sign-up/', sign_up, name='sign-up'),
    path('verify-email/', verify_email, name='verify_email'),
    path('logout/', logout_view, name='logout')
]
