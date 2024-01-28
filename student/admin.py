from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(StudentInfo)
admin.site.register(StudentCertificate)
admin.site.register(WorkExperience)
admin.site.register(Project)