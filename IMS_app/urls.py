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
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, register, dashboard, calendar_view, upload_excel, student_list, student_create, student_update, student_delete, student_info

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', dashboard, name='dashboard'),
    path('calendar/', calendar_view, name="calendar"),
    path('upload-excel/', upload_excel, name='upload_excel'),
    path('show_students/', student_list, name='student_list'),
    path('create/', student_create, name='student_create'),
    path('update/<int:pk>/', student_update, name='student_update'),
    path('delete/<int:pk>/', student_delete, name='student_delete'),
    path('other_info/<int:pk>', student_info, name='other_info'),
]
