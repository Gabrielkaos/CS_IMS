"""
URL configuration for IMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import register, dashboard,  upload_excel, \
    student_list, student_update, student_delete, student_info, logoutView, \
    loginView, faculty_list, faculty_update, faculty_info,\
        subject_list, subject_create, subject_update, subject_delete, subject_info, \
     update_grades, grade_list, upload_grades, save_grades, add_admin_view

urlpatterns = [

    #login
    path('login/', loginView, name='login'),
    path('register/', register, name='register'),
    path('logout/', logoutView, name='logout'),
    path('', dashboard, name='dashboard'),

    #subjects
    path("subject_list/",subject_list,name="subject_list"),
    path('subject_create/', subject_create, name='subject_create'),
    path('subject_update/<int:pk>/', subject_update, name='subject_update'),
    path('subject_delete/<int:pk>/', subject_delete, name='subject_delete'),
    path('subject_info/<int:pk>/',subject_info, name='subject_info'),


    #faculty
    path('show_faculty/', faculty_list, name='faculty_list'),
    path('faculty_update/<int:pk>/', faculty_update, name='faculty_update'),
    path('faculty_info/<int:pk>', faculty_info, name='faculty_info'),


    #students
    path('show_students/', student_list, name='student_list'),
    path('update/<int:pk>/', student_update, name='student_update'),
    path('delete/<int:pk>/', student_delete, name='student_delete'),
    path('other_info/<int:pk>', student_info, name='other_info'),
    path('upload-excel/', upload_excel, name='upload_excel'),

    #grades
    path('show_grades/',grade_list, name='grade_list'),
    path('upload-grades/', upload_grades, name='upload_grades'),
    path('update_grades/<int:pk>', update_grades, name='update_grades'),
    path('grades/<int:pk>/save/', save_grades, name='save_grades'),

    #admin
    path('admin-tools/add-admin/', add_admin_view, name='add_admin')

]
