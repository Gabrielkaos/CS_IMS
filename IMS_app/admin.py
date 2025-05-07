from django.contrib import admin
from .models import Student, Faculty, Subject, Course

# Register your models here.
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Faculty)
