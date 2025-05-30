from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Faculty(models.Model):

    name = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.name}"

class Student(models.Model):

    name = models.CharField(max_length=1000)
    student_id = models.CharField(max_length=50)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    section = models.CharField(max_length=10) # example 1C, 2B
    year_level = models.IntegerField()

    # subjects = models.ForeignKey('Subject', related_name='students')
    subjects = models.ManyToManyField('Subject', through='Enrollment', related_name='students')

    def __str__(self):
        
        return f"{self.name} ({self.student_id})"

class Subject(models.Model):
    code = models.CharField(max_length=10, unique=True)   
    description = models.TextField(blank=True)

    #instructors = connected to Faculty many to many because there could be multiple faculty teaching one subject
    instructors = models.ManyToManyField('Faculty', related_name='subjects')
    # students = models.ManyToManyField('Student', related_name='students')

    def __str__(self):
        return f"{self.code} - {self.description}"
    


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    mid = models.FloatField()
    finals = models.FloatField()

    @property
    def average(self):
        return round((self.mid + self.finals) / 2, 2)

class Enrollment(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    midterm_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    finals_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    semester = models.CharField(max_length=10, blank=True)
    school_year = models.CharField(max_length=9, blank=True)  # e.g., '2024-2025'

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return f"{self.student} - {self.subject} ({((self.midterm_grade + self.finals_grade)/2):.2f})"
