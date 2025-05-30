from django.contrib import admin
from .models import Student, Faculty, Subject, Course, Grade, Enrollment, EnrollmentSubject

# Register your models here.
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Grade)
admin.site.register(Enrollment)
admin.site.register(EnrollmentSubject)