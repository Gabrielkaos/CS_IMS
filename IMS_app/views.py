from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from django.contrib.auth import authenticate, login, logout
from .forms import StudentForm, UploadFileForm
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
import json
import openpyxl
import os

def get_provinces():
    # Load provinces from the local JSON file
    file_path = os.path.join(os.path.dirname(__file__),'static/IMS_app', 'api/provinces.json')
    with open(file_path, 'r') as file:
        provinces = json.load(file)

    # Sort provinces alphabetically by the name
    provinces = sorted(provinces, key=lambda x: x['name'])
    return provinces

def get_province_code(name):
    if not name:
        return ""
    file_path = os.path.join(os.path.dirname(__file__),'static/IMS_app', 'api/provinces.json')
    with open(file_path, 'r') as file:
        provinces = json.load(file)
    for province in provinces:
        if province.get("name", "").lower() == name.lower():
            return province.get("code", "")
    return ""

def get_city_code(name):
    if not name:
        return ""
    file_path = os.path.join(os.path.dirname(__file__),'static/IMS_app', 'api/cities-municipalities.json')
    with open(file_path, 'r') as file:
        cities = json.load(file)
    for city in cities:
        if city.get("name", "").lower() == name.lower():
            return city.get("code", "")
    return ""

def get_barangay_code(name):
    if not name:
        return ""
    file_path = os.path.join(os.path.dirname(__file__),'static/IMS_app', 'api/barangays.json')
    with open(file_path, 'r') as file:
        barangays = json.load(file)
    for barangay in barangays:
        if barangay.get("name", "").lower() == name.lower():
            return barangay.get("code", "")
    return ""

def calendar_view(request):
    students = Student.objects.all()
    birthdays = [
        {
            "name": student.name,
            "date": student.date_of_birth.strftime('%Y-%m-%d')
        }
        for student in students
    ]
    return render(request, "IMS_app/calendar.html", {
        "birthdays_json": json.dumps(birthdays, cls=DjangoJSONEncoder)
    })

def upload_excel(request):
    if request.method == 'POST':
        print("Hello there")
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # excel_file = request.FILES['excel_file']
            # df = pd.read_excel(excel_file)
            excel_file = request.FILES['files']
            # df = pd.read_excel(excel_file)
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                first_name, middle_name, last_name, student_id, year_level, status, email, date_of_birth,gender,phone_number, current_province, current_city, current_barangay, permanent_province, permanent_city, permanent_barangay, emergency_contact_name,\
                emergency_contact_phone, emergency_contact_relation = row
                Student.objects.create(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    student_id=student_id,
                    year_level=year_level,
                    status=status,
                    email=email,
                    date_of_birth=date_of_birth,
                    gender=gender[0].upper(),
                    phone_number=phone_number,
                    current_province_code=get_province_code(current_province.title()),
                    current_city_code=get_city_code(current_city.title()),
                    current_barangay_code=get_barangay_code(current_barangay.title()),
 
                    permanent_province_code=get_province_code(permanent_province.title()),
                    permanent_city_code=get_city_code(permanent_city.title()),
                    permanent_barangay_code=get_barangay_code(permanent_barangay.title()),
                    emergency_contact_name=emergency_contact_name.title(),
                    emergency_contact_phone=emergency_contact_phone,
                    emergency_contact_relation=emergency_contact_relation[0].upper()
                )
            messages.success(request, "Excel file uploaded successfully!")
            return redirect('student_list')
    else:
        form = UploadFileForm(request.POST, request.FILES)
        # print("Hello the/re 2")
    return redirect('student_list')

# Accounts
def register(request):
    # print("Hello")
    if request.method == "POST":
        # print("HGello")
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        role = request.POST["role"]

        if password != password2:
            messages.error(request, "Wrong password confirmation")
            return redirect("register")

        user, created = User.objects.get_or_create(username=username)

        if created:
            user.set_password(password)
            user.is_staff = True
            if role=="admin":
                user.is_superuser = True
            else:
                user.is_superuser = False
            user.save()
            messages.success(request, "User created")
            return render(request, "IMS_app/login.html")

        else:
            messages.error(request, "User already exists")
            return redirect("register")

    return render(request, "IMS_app/register.html")

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        print(role)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'IMS_app/login.html')


@login_required
def dashboard(request):
    total_students = Student.objects.count()

    # Gender distribution
    gender_counts = Student.objects.values('gender').annotate(count=Count('gender'))
    gender_data = {
        'Male': 0,
        'Female': 0,
        'Other': 0,
        'Unspecified': 0
    }
    for item in gender_counts:
        key = dict(Student.GENDER_CHOICES).get(item['gender'], 'Unspecified')
        gender_data[key] = item['count']

    # Students per year level
    year_level_data = Student.objects.values('year_level').annotate(count=Count('year_level')).order_by('year_level')

    # Age statistics
    from datetime import date
    def calculate_age(dob):
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    ages = [calculate_age(student.date_of_birth) for student in Student.objects.all() if student.date_of_birth]
    average_age = sum(ages) / len(ages) if ages else 0
    min_age = min(ages) if ages else 0
    max_age = max(ages) if ages else 0

    context = {
        'total_students': total_students,
        'gender_data': gender_data,
        'year_level_data': year_level_data,
        'average_age': round(average_age, 1),
        'min_age': min_age,
        'max_age': max_age,
    }

    return render(request, 'IMS_app/dashboard.html', context)

def student_info(request, pk):
    student = get_object_or_404(Student, pk=pk)
    # print('Student!!!!!!!!!!!!!:',student)
    return render(request, 'IMS_app/student_other_info.html', {'student': student})

@login_required
def student_list(request):
    students = Student.objects.all()
    form = UploadFileForm()
    return render(request, 'IMS_app/student_list.html', {'students': students, 'form':form})

@login_required
def student_create(request):
    provinces = get_provinces()
    if request.method == 'POST':
        form = StudentForm(request.POST, provinces=provinces)
        if form.is_valid():
            print('create form cleaned:',form.cleaned_data)
            form.save()
            print("This is the form",form)
            return redirect('student_list')
    else:
        form = StudentForm(provinces=provinces)
    return render(request, 'IMS_app/student_form.html', {'form': form, 'provinces': provinces})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    provinces = get_provinces()
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student, provinces=provinces)
        if form.is_valid():
            print('update form cleaned:',form.cleaned_data)
            form.save()
            print("This is the form",form)
            return redirect('student_list')
    else:
        form = StudentForm(instance=student, provinces=provinces)
    return render(request, 'IMS_app/student_form.html', {'form': form, 'provinces': provinces})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'IMS_app/student_confirm_delete.html', {'student': student})

def logoutView(req):

    logout(req)

    return redirect("login")