from django import forms
from .models import Student, Faculty, Subject, Course, Grade
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AdminCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")  # You can add more fields if needed

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['code', 'description']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'mid', 'finals']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']
        widgets = {
            'name': forms.TextInput()
        }


class UploadFileForm(forms.Form):
    files = forms.FileField()

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name','student_id']


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'
        