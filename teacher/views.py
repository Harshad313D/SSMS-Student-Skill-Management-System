import os
from sqlite3 import IntegrityError
import io
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from student.models import Student, StudentInfo
from account.models import User
from .models import *
from ssms import settings
import pandas as pd
from xlsxwriter import *


@login_required
def teacher_dashboard(request):
    context = {}
    teacher_info = TeacherInfo.objects.get(teacher__email=request.user.email)
    students = StudentInfo.objects.all()
    context['teacher_info'] = teacher_info
    context['students'] = students
    return render(request, "teacher/teacher_dashboard.html", context)


@login_required
def add_student(request):
    context = {}

    if request.method == 'POST':
        batu_prn = request.POST.get('batu_prn')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number', '')

        try:
            # Check if a student with the same email or BATU PRN already exists
            existing_student = Student.objects.filter(email=email, batu_prn=batu_prn).first()

            if existing_student:
                context["error"] = "Student with the same email or BATU PRN already exists."
            else:
                # Create a new student instance and save it to the database
                student = Student(
                    batu_prn=batu_prn,
                    email=email,
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    phone_number=phone_number
                )
                student.save()

                # Create a random password for the user
                password = student.batu_prn

                # Create a User object
                user = User.objects.create_user(
                    email=student.email,
                    password=password,
                    first_name=student.first_name,
                    last_name=student.last_name,
                    student_obj=student,
                )
                user.save()

                student_info = StudentInfo(student=student)
                student_info.save()

                context["message"] = "Student added successfully."

        except IntegrityError:
            # Handle IntegrityError, for example, if there's a unique constraint violation
            context["error"] = "An error occurred while saving the student. Please try again."

    return render(request, 'teacher/add_student.html', context)


@login_required
def upload_student_excel(request):
    context = {
        'heading': "Upload Students Excel",
        'sub_heading': "Add Students using an excel sheet, choose the file and upload to insert the students"
    }

    try:
        if request.method == 'POST' and request.FILES['excel_file']:
            excel_file = request.FILES['excel_file']
            students_already_exist = []
            # Start a database transaction
            with transaction.atomic():
                # Assuming the first sheet in the Excel file contains the data
                df = pd.read_excel(excel_file)

                # Loop through the rows of the DataFrame and insert data into the model
                for index, row in df.iterrows():
                    try:
                        student_instance = Student.objects.get(email=row['email'])
                        students_already_exist.append(student_instance)
                        # Do something with the student_instance
                    except Student.DoesNotExist:
                        student_data = {
                            'batu_prn': row['batu'],
                            'email': row['email'],
                            'first_name': row['fname'],
                            'middle_name': row['mname'],
                            'last_name': row['lname'],
                            'phone_number': row['phone_no'],
                        }

                        # Create a new Student object and save it to the database
                        student = Student(**student_data)
                        student.save()

                        # Create a User object
                        user = User.objects.create_user(
                            email=student.email,
                            password=str(student.batu_prn),
                            first_name=student.first_name,
                            last_name=student.last_name,
                            student_obj=student,
                        )
                        user.save()

                        student_info = StudentInfo(student=student)
                        student_info.save()
            context["students_already_exist"] = students_already_exist
            context["message"] = "Students Uploaded Successfully"

    except Exception as e:
        # Handle the exception and add the error message to the context
        context['error'] = "An error occurred: " + str(e)

    return render(request, 'teacher/upload.html', context)


@login_required
def download_sample_file(request):
    # Path to the sample file in your media directory
    sample_file_path = os.path.join(settings.MEDIA_ROOT, 'sample_file.xlsx')

    # Open and serve the file
    try:
        sample_file = open(sample_file_path, 'rb')
        response = FileResponse(sample_file)
        response['Content-Disposition'] = 'attachment; filename="sample_file.xlsx"'
        return response
    except FileNotFoundError:
        # Handle the case when the sample file is not found
        raise Http404('Sample file not found')



@login_required
def display_student(request):
    context = {}
    teacher_info = TeacherInfo.objects.get(teacher__email=request.user.email)

    students = StudentInfo.objects.all()

    if request.method == 'POST':
        gender = request.POST.get('gender')
        division = request.POST.get('division')
        language = request.POST.get('language')

        filter_params = {}

        if gender:
            filter_params['gender'] = gender

        if division:
            filter_params['division'] = division

        if language:
            filter_params['preferred_language'] = language

        # Apply the filter only with non-empty/non-None parameters
        students = StudentInfo.objects.filter(**filter_params)
        return filter_and_export(students)

    context['teacher_info'] = teacher_info
    context['students'] = students
    return render(request, "teacher/display_student.html", context)


def filter_and_export(students):
    data = {
        'batu': students.values_list('student__batu_prn', flat=True),
        'fname': students.values_list('student__first_name', flat=True),
        'mname': students.values_list('student__middle_name', flat=True),
        'lname': students.values_list('student__last_name', flat=True),
        'email': students.values_list('student__email', flat=True),
        'phone': students.values_list('student__phone_number', flat=True),
    }

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="filtered_students.xlsx"'

    df.to_excel(response, index=False)
    return response

    # return render(request, "teacher/display_student.html", context)