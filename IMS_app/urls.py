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
from .views import register, dashboard, calendar_view, upload_excel, \
    student_list, student_create, student_update, student_delete, student_info, logoutView, \
    loginView, faculty_list, faculty_update, faculty_create, faculty_delete, faculty_info,\
    upload_faculty

urlpatterns = [
    path('login/', loginView, name='login'),
    path('register/', register, name='register'),
    path('logout/', logoutView, name='logout'),
    path('', dashboard, name='dashboard'),
    path('calendar/', calendar_view, name="calendar"),
    path('upload-excel/', upload_excel, name='upload_excel'),
    
    path('upload-faculty/', upload_faculty, name='upload_faculty'),
    path('show_faculty/', faculty_list, name='faculty_list'),
    path('faculty_update/<int:pk>/', faculty_update, name='faculty_update'),
    path('faculty_create/', faculty_create, name='faculty_create'),
    path('faculty_delete/<int:pk>/', faculty_delete, name='faculty_delete'),
    path('faculty_info/<int:pk>', faculty_info, name='faculty_info'),

    path('show_students/', student_list, name='student_list'),
    path('create/', student_create, name='student_create'),
    path('update/<int:pk>/', student_update, name='student_update'),
    path('delete/<int:pk>/', student_delete, name='student_delete'),
    path('other_info/<int:pk>', student_info, name='other_info'),
]
