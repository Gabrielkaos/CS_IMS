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
    student_id = models.CharField(max_length=50,unique=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    # section = models.CharField(max_length=10) # example 1C, 2B
    # year_level = models.IntegerField()
    # school_year = models.CharField(max_length=9)
    # semester = models.IntegerField()

    # subjects = models.ForeignKey('Subject', related_name='students')
    # subjects = models.ManyToManyField('Subject', related_name='students')

    def __str__(self):
        return f"{self.name} ({self.student_id})"

class Subject(models.Model):
    code = models.CharField(max_length=10, unique=True)   
    description = models.CharField(max_length=500, unique=True)

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
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    school_year = models.CharField(max_length=9)  # e.g., '2024-2025'
    semester = models.IntegerField()
    year_level = models.IntegerField()
    section = models.CharField(max_length=10, blank=True, null=True)
    # Use a through model
    subjects = models.ManyToManyField('Subject', through='EnrollmentSubject', related_name='enrollments')

    class Meta:
        unique_together = ('student', 'school_year', 'semester')

    def __str__(self):
        return f"{self.student.name} - {self.school_year} S{self.semester}"
    
class EnrollmentSubject(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    midterm_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    final_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        unique_together = ('enrollment', 'subject')

    @property
    def average(self):
        average = 0
        if self.midterm_grade is not None and self.final_grade is not None:
            average = round((self.midterm_grade + self.final_grade)/2,2)
        return average

    def __str__(self):
        average = None
        if self.midterm_grade is not None and self.final_grade is not None:
            average = round((self.midterm_grade + self.final_grade)/2,2)
        return f"{self.enrollment.student.name} - {self.subject.description} - {average}"


