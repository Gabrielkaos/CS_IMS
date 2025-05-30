from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Faculty, Subject, Course, Grade
from django.contrib.auth import authenticate, login, logout
from .forms import StudentForm, UploadFileForm, FacultyForm, SubjectForm, CourseForm, GradeForm
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import openpyxl

sections = "1A,1B,1C,2A,2B,2C,3A,3B,3C,4A,4B,4C,1,2,3,4".split(",")

def upload_excel(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['files']
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active

            # Extract metadata
            course_and_section = sheet['C7'].value
            section = str(course_and_section).split()[1]
            code = sheet['C8'].value
            subject_description = sheet['C9'].value
            instructor_name = sheet['C10'].value

            sem_sy = sheet['C4'].value
            semester1 = str(sem_sy).split(",")[0].lower()
            sy = str(sem_sy).split(",")[1].strip()

            real_sem = None
            if semester1.startswith("first"):
                real_sem = 1
            elif semester1.startswith("second"):
                real_sem = 2
            else:
                real_sem = 3

            # Get or create Course
            course_obj, _ = Course.objects.get_or_create(name=str(course_and_section).split()[0])

            # Get or create Subject
            subject_obj, _ = Subject.objects.get_or_create(
                code=code,
                defaults={'description': subject_description}
            )

            # Get or create Faculty
            faculty_obj, _ = Faculty.objects.get_or_create(name=instructor_name)

            # You can add M2M linking here if needed:
            subject_obj.instructors.add(faculty_obj)

            # Iterate through students starting from row 12
            for row in sheet.iter_rows(min_row=12, values_only=True):
                if not row[1] or not row[2]:
                    continue
                student_id = str(row[1]).strip()
                name = row[2].strip()

                if student_id.startswith("---"):continue

                student_obj, _ = Student.objects.get_or_create(
                    student_id=student_id,
                    course = course_obj,
                    year_level = int(list(section)[0]),
                    semester = real_sem,
                    school_year = sy,
                    defaults={'name': name, 'section': section}
                )
                student_obj.subjects.add(subject_obj)

            return redirect("student_list")
        form = UploadFileForm()
    return redirect("student_list")

# Accounts
def register(request):
    # print("Hello")
    if request.method == "POST":
        # print("HGello")
        print("I am in registerView")
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            password2 = request.POST["password2"]
            # role = request.POST["role"]
        except:
            password2 = password
            # role = "student"
        

        if password != password2:
            messages.error(request, "Wrong password confirmation")
            return redirect("register")

        user, created = User.objects.get_or_create(username=username)

        if created:
            user.set_password(password)
            
            user.is_superuser = True
            user.is_staff = True
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
        print("I am in loginView")
        
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


    # Students per year level
    year_level_data = Student.objects.values('year_level').annotate(count=Count('year_level')).order_by('year_level')

    context = {
        'total_students': total_students,
        'year_level_data': year_level_data
    }

    return render(request, 'IMS_app/dashboard.html', context)

def student_info(request, pk):
    student = get_object_or_404(Student, pk=pk)
    # print('Student!!!!!!!!!!!!!:',student)
    return render(request, 'IMS_app/student_other_info.html', {'student': student})

def faculty_info(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    subjects1 = faculty.subjects.all()
    print(subjects1)
    return render(request, 'IMS_app/faculty_info.html', {'faculty': faculty,"subjects":subjects1})

def subject_info(request, pk):
    course = get_object_or_404(Subject, pk=pk)
    return render(request, 'IMS_app/subject_info.html', {'course': course})

@login_required
def student_list(request):
    school_years = []
    school_year = request.GET.get('school_year')
    semester = request.GET.get('semester')

    students = Student.objects.all()

    for student in students:
        if student.school_year not in school_years:
            school_years.append(student.school_year)

    if school_year:
        students = students.filter(school_year=school_year)
    if semester:
        students = students.filter(semester=semester)

    form = UploadFileForm()
    return render(request, 'IMS_app/student_list.html', 
                  {'students': students, 
                   'form':form, 
                   "semesters":[1,2,3],
                   "school_years":school_years,
                   "selected_year":school_year,
                   "selected_semester":semester})
@login_required
def faculty_list(request):
    faculties = Faculty.objects.all()
    form = UploadFileForm()
    return render(request, 'IMS_app/faculty_list.html', {'faculties': faculties, 'form':form})

@login_required
def subject_list(request):
    coursies = Subject.objects.all()
    return render(request, 'IMS_app/subject_list.html', {'coursies': coursies})

@login_required
def subject_create(request):
    instructors = Faculty.objects.all()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            # print('create form cleaned:',form.cleaned_data)
            form1 = form.save(commit=False)
            instructor = Faculty.objects.get(id=request.POST["faculties"])
            print(request.POST["faculties"])
            form1.instructor = instructor
            # print("This is the form",form)
            form1.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'IMS_app/subject_form.html', {'form': form, 'instructors':instructors})

@login_required
def subject_update(request, pk):
    course = get_object_or_404(Subject, pk=pk)
    instructors = Faculty.objects.all()
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=course)
        if form.is_valid():
            # print('update form cleaned:',form.cleaned_data)
            form1 = form.save(commit=False)
            instructor = Faculty.objects.get(id=request.POST["faculties"])
            print(request.POST["faculties"])
            form1.instructor = instructor
            # print("This is the form",form)
            form1.save()
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=course)
    return render(request, 'IMS_app/subject_form.html', {'form': form,"instructors":instructors})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    coursies = Course.objects.all()
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            print("Form valid student update")
            form1 = form.save()
            
            course = Course.objects.get(id=request.POST["course"])
            form1.course = course

            form1.section = request.POST["section"]
            form1.year_level = int(list(request.POST["section"])[0])

            form1.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'IMS_app/student_form.html', {'form': form,'coursies':coursies, "student":student, "sections":sections})

@login_required
def faculty_update(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        form = FacultyForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            return redirect('faculty_list')
    else:
        form = FacultyForm(instance=faculty)
    return render(request, 'IMS_app/faculty_form.html', {'form': form})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('student_list')

def subject_delete(request, pk):
    course = get_object_or_404(Subject, pk=pk)
    course.delete()
    return redirect('subject_list')


def course_list(request):
    
    coursies = Course.objects.all()
    students = Student.objects.all()

    first = 0; second = 0; third = 0; fourth = 0;

    for student in students:
        if student.year_level == 1:
            first+=1
        elif student.year_level == 2:
            second+=1
        elif student.year_level == 3:
            third+=1
        else:
            fourth+=1

    return render(request, 'IMS_app/course_list.html', {'first':first,'second':second,'third':third,'fourth':fourth})

def logoutView(req):

    logout(req)

    return redirect("login")


def update_grades(req, pk):
    student = get_object_or_404(Student, pk=pk)
    subjects = Subject.objects.all()
    # Get all grades related to this student
    grades = Grade.objects.filter(student=student).select_related('subject')
    
    return render(req, 'IMS_app/grades.html', {
        'student': student,
        'grades': grades,
        'subjects':subjects
    })
    
def add_grade(request, pk):
    if request.method == 'POST':
        student = get_object_or_404(Student,pk=pk)
        Grade.objects.create(
            student = student, 
            subject = Subject.objects.get(id=request.POST.get("course")),
            mid = float(request.POST.get("mid")),
            finals = float(request.POST.get("finals")),
                    )
        return redirect("student_list")