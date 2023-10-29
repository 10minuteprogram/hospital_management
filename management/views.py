from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def home(request):

    return render(request, 'management/home.html')

def manage_doctor(request):

    depertment = MedicalDepartment.objects.all()
    specialist = Specialist.objects.all()
    doctors = MedicalDoctor.objects.all()

    context = {
        'depertment': depertment,
        'specialist':specialist,
        'doctors':doctors
    }

    return render(request, 'management/manage_doctor.html', context)

def new_department(request):

    if request.method == 'POST':
        name = request.POST.get('dpt_name')
        created_by = request.user

        try:
            MedicalDepartment.objects.create(
                name=name,
                created_by = created_by
            )
        except Exception as e:
            print(type(e))
            if "UNIQUE constraint failed:" in str(e):
                message = f"Duplicate department name {name} is not allowed"
            else:
                message = e
            messages.error(request, message)

        return redirect('manage_doctor')
    superusers = User.objects.filter(is_superuser=True)
    context = {
        'superusers':superusers
    }
    return render(request, 'management/new_department.html',context)


def new_specialist(request):
    if request.method == 'POST':
        specialist_name = request.POST.get('specialist_name')
        Specialist.objects.create(
            title = specialist_name
        )
        return redirect('manage_doctor')
    return render(request, 'management/new_specialist.html')


def new_doctor(request):
    if request.method == 'POST':
        doctor_name = request.POST.get('doctor_name')
        doctor_image=request.FILES.get('doctor_image')
        created_by = request.user

        MedicalDoctor.objects.create(
            name = doctor_name,
            image = doctor_image,
            created_by = created_by
        )

        return redirect('manage_doctor')

    superusers = User.objects.filter(is_superuser=True)
    context = {
        'superusers':superusers
    }
    return render(request, 'management/new_doctor.html',context)