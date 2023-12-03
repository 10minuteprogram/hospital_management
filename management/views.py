from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import random
from hospital_management.postman import send_email

# Create your views here.
@login_required(login_url='/sign-in/')
def home(request):    
    return render(request, 'management/home.html')

@login_required(login_url='/sign-in/')
def manage_doctor(request):
    depertment = MedicalDepartment.objects.all()
    specialist = Specialist.objects.all()
    doctors = MedicalDoctor.objects.all()

    # filter doctors by department
    dept = request.GET.get('department')
    if dept:
        doctors = doctors.filter(department__name=dept)

    search = request.GET.get('search')
    if search:
        doctors = doctors.filter(Q(name__icontains=search) | Q(hospital__icontains=search))

    context = {
        'depertment': depertment,  # Correct the typo in the variable name
        'specialist': specialist,
        'doctors': doctors
    }

    return render(request, 'management/manage_doctor.html', context)

@login_required(login_url='/sign-in/')
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

        context = {
                'random_number': 272632367
            }

        doctors_with_image = MedicalDoctor.objects.filter(image__isnull=False)
        files = []
        for doctor in doctors_with_image:
            if doctor.image:
                files.append(doctor.image.path)
        

        result = send_email(
            "New Department Added!!!!!",
            ['10minuteprogram@gmail.com', 'majedkhan420.m4@gmail.com'],
            'management/emails/activation.html',
            context,
            files
        )
        print(result)

        return redirect('manage_doctor')
    
    superusers = User.objects.filter(is_superuser=True)
    context = {
        'superusers':superusers
    }
    return render(request, 'management/new_department.html',context)

@login_required(login_url='/sign-in/')
def new_specialist(request):
    if request.method == 'POST':
        specialist_name = request.POST.get('specialist_name')
        Specialist.objects.create(
            title = specialist_name
        )
        return redirect('manage_doctor')
    return render(request, 'management/new_specialist.html')

@login_required(login_url='/sign-in/')
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

@login_required(login_url='/sign-in/')
def profile(request):

    return render(request, 'management/profile.html')

@login_required(login_url='/sign-in/')
def edit_profile(request):

    return render(request, 'management/edit_profile.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                message = "invalid username and password"
        else:
            message = "username and password reqired"
    context = {
        'message':message
    }
    return render(request, 'management/signin.html', context)

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
 
        # Create a new user
        if username and email and password:
            # check if user already exists
            has_already = User.objects.filter(username=username).first()
            if has_already:
                messages.error(request, f"Username {username} already exists")
                return redirect('sign-up')
            # check if email already exists
            has_already = User.objects.filter(email=email).first()
            if has_already:
                messages.error(request, f"Email {email} already exists")
                return redirect('sign-up')

            user = User.objects.create_user(username=username, email=email, password=password)
            
            # geneate random otp
            otp = random.randint(100000,999999)

            user.profile.email_verification_code = otp
            user.profile.save()
            user.save()
            context = {
                'otp': otp,
                'username': username,
            }
            response = send_email('Verify your 10MP account', [email], 'management/emails/email_verification.html', context, [])
            print(response)
            # Log in the user after registration
            login(request, user)
            messages.success(request, 'Singin successfully')
            return redirect('home')
        else:
            messages.error(request, "All the fields are required")
            return redirect('sign-up')
        
    
    return render(request, 'management/sign_up.html')

@login_required(login_url='/sign-in/')
def verify_email(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_otp = request.user.profile.email_verification_code
        if otp == user_otp:
            request.user.profile.is_email_active = True
            request.user.save()
            return redirect('home')
        else:
            messages.error(request, "Invalid OTP Entered")
            return redirect('verify_email')


    return render(request, 'management/verify_email.html')

@login_required(login_url='/sign-in/')
def logout_view(request):
    logout(request)
    return redirect('sign-in')