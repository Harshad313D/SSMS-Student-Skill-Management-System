from datetime import datetime

from django.db import models


class Student(models.Model):
    batu_prn = models.CharField(max_length=20, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.email


class StudentInfo(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)

    # Academic Records
    division = models.CharField(max_length=10, null=True, blank=True)
    preferred_language = models.CharField(max_length=20, null=True, blank=True)

    c_degree = models.CharField(max_length=75, null=True, blank=True)
    c_department = models.CharField(max_length=100, null=True, blank=True)
    current_year = models.PositiveIntegerField(null=True, blank=True)
    current_semester = models.PositiveIntegerField(null=True, blank=True)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    # Secondary School Information
    ss_name = models.CharField(max_length=10, null=True, blank=True)
    ss_school_name = models.CharField(max_length=50, null=True, blank=True)
    ss_start_year = models.DateField(null=True, blank=True)
    ss_end_year = models.DateField(null=True, blank=True)
    ss_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Primary School Information
    ps_name = models.CharField(max_length=10, null=True, blank=True)
    ps_school_name = models.CharField(max_length=50, null=True, blank=True)
    ps_start_year = models.DateField(null=True, blank=True)
    ps_end_year = models.DateField(null=True, blank=True)
    ps_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Profile
    designation = models.CharField(max_length=100, null=True, blank=True)
    experience_years = models.PositiveIntegerField(null=True, blank=True, default=0)
    gender = models.CharField(max_length=10, blank=True, null=True)

    about_me = models.TextField(max_length=300, null=True, blank=True)

    technical_skills = models.CharField(max_length=200, null=True, blank=True)
    soft_skills = models.CharField(max_length=200, null=True, blank=True)

    github = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.student.first_name} {self.student.middle_name} {self.student.last_name}'


class StudentCertificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    certificate_name = models.CharField(max_length=250)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    link = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} {self.certificate_name}"


class WorkExperience(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    key_points = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.email}: {self.organization_name} - {self.start_date} to {self.end_date}"


class Project(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    key_points = models.TextField()
    link = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.email}: {self.project_name} - {self.start_date} to {self.end_date}"

