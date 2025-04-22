import os
import json
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile", null=True, blank=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    YEAR_LEVEL_CHOICES = [(i, str(i)) for i in range(1, 5)]

    RELATIONSHIP_CHOICES = [
        ('P', 'Parent'),
        ('S', 'Sibling'),
        ('G', 'Guardian'),
        ('O', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Regular', 'Regular'),
        ('Irregular', 'Irregular'),
        ('Other', 'Other')
    ]

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=9, unique=True)
    year_level = models.IntegerField(choices=YEAR_LEVEL_CHOICES, blank=False)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

    # Current Address
    current_province_code = models.CharField(max_length=10, blank=True)
    current_city_code = models.CharField(max_length=10, blank=True)
    current_barangay_code = models.CharField(max_length=10, blank=True)

    # Permanent Address
    permanent_province_code = models.CharField(max_length=10, blank=True)
    permanent_city_code = models.CharField(max_length=10, blank=True)
    permanent_barangay_code = models.CharField(max_length=10, blank=True)


    # emergency contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    emergency_contact_relation = models.CharField(choices=RELATIONSHIP_CHOICES, max_length=50, blank=True)
    
    @property
    def name(self):
        if self.middle_name:
            return f"{self.last_name}, {self.first_name} {self.middle_name[0]}."
        return f"{self.last_name}, {self.first_name}"
    
    @property
    def current_address(self):
        print("From models here!!!!!!!!!!!!!!!!\n",self.current_province_code)
        print("Name:", self.name)
        return f"{self.get_barangay_name(self.current_barangay_code)}, {self.get_city_name(self.current_city_code)}, {self.get_province_name(self.current_province_code)}"

    @property
    def permanent_address(self):
        return f"{self.get_barangay_name(self.permanent_barangay_code)}, {self.get_city_name(self.permanent_city_code)}, {self.get_province_name(self.permanent_province_code)}"

    def get_province_name(self, code):
        if not code:
            return ""
        file_path = os.path.join(os.path.dirname(__file__), 'api/provinces.json')
        with open(file_path, 'r') as file:
            provinces = json.load(file)
        for province in provinces:
            if province.get("code", "") == code:
                return province.get("name", "")
        return ""

    def get_city_name(self, code):
        if not code:
            return ""
        file_path = os.path.join(os.path.dirname(__file__), 'api/cities-municipalities.json')
        with open(file_path, 'r') as file:
            cities = json.load(file)
        for city in cities:
            if city.get("code", "") == code:
                return city.get("name", "")
        return ""

    def get_barangay_name(self, code):
        if not code:
            return ""
        file_path = os.path.join(os.path.dirname(__file__), 'api/barangays.json')
        with open(file_path, 'r') as file:
            barangays = json.load(file)
        for barangay in barangays:
            if barangay.get("code", "") == code:
                return barangay.get("name", "")
        return ""

    def __str__(self):
        return f"{self.name} ({self.student_id})"








