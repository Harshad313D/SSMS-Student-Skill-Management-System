from django.db import models


class Teacher(models.Model):
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return self.email


class TeacherInfo(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_info')
    date_of_birth = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100)
    subjects_taught = models.TextField(blank=True, null=True)
    qualifications = models.TextField(null=False)
    years_of_experience = models.CharField(max_length=10, blank=True, null=True)
    certification = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.teacher.first_name} {self.teacher.last_name}"

