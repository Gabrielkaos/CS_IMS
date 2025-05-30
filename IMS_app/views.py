from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Faculty, Subject, Course, Grade, Enrollment,EnrollmentSubject
from django.contrib.auth import authenticate, login, logout
from .forms import StudentForm, UploadFileForm, FacultyForm, SubjectForm
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import openpyxl


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
            semester_str = str(sem_sy).split(",")[0].lower()
            sy = str(sem_sy).split(",")[1].strip()

            if semester_str.startswith("first"):
                real_sem = 1
            elif semester_str.startswith("second"):
                real_sem = 2
            else:
                real_sem = 3

            year_level = int(section[0]) if section[0].isdigit() else 1

            course_obj, _ = Course.objects.get_or_create(name=str(course_and_section).split()[0])

            subject_obj, _ = Subject.objects.get_or_create(
                code=code,
                defaults={'description': subject_description}
            )

            faculty_obj, _ = Faculty.objects.get_or_create(name=instructor_name)
            subject_obj.instructors.add(faculty_obj)

            for row in sheet.iter_rows(min_row=12, values_only=True):
                if not row[1] or not row[2]:
                    continue
                student_id = str(row[1]).strip()
                name = row[2].strip()

                if student_id.startswith("---"):
                    continue

                student_obj, _ = Student.objects.get_or_create(
                    student_id=student_id,
                    defaults={'name': name, 'course': course_obj}
                )
                print(section)
                enrollment_obj, _ = Enrollment.objects.get_or_create(
                    student=student_obj,
                    school_year=sy,
                    semester=real_sem,
                    defaults={
                        'year_level': year_level,
                        'section': list(section)[1] if len(section)>1 else section
                    }
                )

                # Link subject to enrollment
                EnrollmentSubject.objects.get_or_create(
                    enrollment=enrollment_obj,
                    subject=subject_obj
                )

            return redirect("student_list")

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
    total_subjects = Subject.objects.count()
    total_faculty = Faculty.objects.count()
    total_enrollments = Enrollment.objects.count()

    current_sy = Enrollment.objects.order_by('-school_year').values_list('school_year', flat=True).first()
    current_sem = Enrollment.objects.order_by('-semester').values_list('semester', flat=True).first()

    # Students per subject (top 5)
    top_subjects = Subject.objects.annotate(student_count=Count('enrollmentsubject__enrollment__student')) \
                                  .order_by('-student_count')[:5]

    # Students per year level
    year_level_data = Enrollment.objects.values('year_level').annotate(count=Count('student'))

    # Students per course
    course_data = Student.objects.values('course__name').annotate(count=Count('id')).order_by('-count')

    return render(request, 'IMS_app/dashboard.html', {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_faculty': total_faculty,
        'total_enrollments': total_enrollments,
        'current_sy': current_sy,
        'current_sem': current_sem,
        'top_subjects': top_subjects,
        'year_level_data': year_level_data,
        'course_data': course_data,
    })

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
    enrolees_on_sub = EnrollmentSubject.objects.filter(subject=course)

    return render(request, 'IMS_app/subject_info.html', {'course': course,'count1':enrolees_on_sub.count()})

@login_required
def student_list(request):
    school_year = request.GET.get('school_year')
    semester = request.GET.get('semester')
    year_level = request.GET.get('year_level')
    subject_id = request.GET.get('subject')

    # Get all students through their enrollments
    students = Student.objects.all()

    if school_year or semester or year_level or subject_id:
        enrollments = Enrollment.objects.all()
        
        if school_year:
            enrollments = enrollments.filter(school_year=school_year)
        if semester:
            enrollments = enrollments.filter(semester=semester)
        if year_level:
            enrollments = enrollments.filter(year_level=year_level)
        if subject_id:
            enrollments = enrollments.filter(
                enrollmentsubject__subject__id=subject_id
            )
        
        students = Student.objects.filter(enrollments__in=enrollments).distinct()

    # Get all school years for dropdown
    school_years = Enrollment.objects.values_list('school_year', flat=True).distinct()
    subjects = Subject.objects.all()

    form = UploadFileForm()
    return render(request, 'IMS_app/student_list.html', {
        'students': students,
        'form': form,
        'semesters': [1, 2, 3],
        'year_levels': [1, 2, 3, 4],
        'school_years': school_years,
        'subjects': subjects,
        'selected_year': school_year,
        'selected_semester': semester,
        'selected_year_level': year_level,
        'selected_subject': subject_id,
        'student_count': students.count()
    })

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
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=course)
        if form.is_valid():
            # print('update form cleaned:',form.cleaned_data)
            form1 = form.save(commit=False)
            # print("This is the form",form)
            form1.save()
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=course)
    return render(request, 'IMS_app/subject_form.html', {'form': form})

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

            form1.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'IMS_app/student_form.html', {'form': form,'coursies':coursies, "student":student})

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