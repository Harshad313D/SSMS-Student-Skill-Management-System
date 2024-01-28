from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse



@login_required
def student_dashboard(request):
    context = {}
    student = StudentInfo.objects.get(student__email=request.user.email)
    projects = Project.objects.filter(student__email=request.user.email).order_by('date_added')

    total_certifications = StudentCertificate.objects.filter(student__email=request.user.email)

    context['student'] = student
    context['total_certifications'] = len(total_certifications)
    context['total_projects'] = len(projects)

    return render(request, "student/student_dashboard.html", context)


def student_profile(request):
    context = {}
    student = StudentInfo.objects.get(student__email=request.user.email)
    projects = Project.objects.filter(student__email=request.user.email).order_by('date_added')
    work = WorkExperience.objects.filter(student__email=request.user.email).order_by('date_added')

    total_certifications = StudentCertificate.objects.filter(student__email=request.user.email)

    tech_skills = []
    soft_skills = []
    work_points = []
    project_points = []

    if student.technical_skills:
        skills_string = student.technical_skills
        tech_skills = [skill.strip() for skill in skills_string.split(',')]

    if student.soft_skills:
        soft_skills_string = student.soft_skills
        soft_skills = [skill.strip() for skill in soft_skills_string.split(',')]

    for i in work:
        work_key_points = []

        if i.key_points:
            key_points_string = i.key_points
            key_points = [skill.strip() for skill in key_points_string.split(',')]
            work_key_points.append(key_points)

        work_points.append(work_key_points)

    for i in projects:
        project_key_points = []

        if i.key_points:
            key_points_string = i.key_points
            key_points = [skill.strip() for skill in key_points_string.split(',')]
            project_key_points.append(key_points)

        project_points.append(project_key_points)

    context['student'] = student
    context['projects'] = zip(projects, project_points)
    context['work'] = zip(work, work_points)
    context['total_certifications'] = len(total_certifications)
    context['total_projects'] = len(projects)
    context['tech_skills'] = tech_skills
    context['soft_skills'] = soft_skills
    context['total_work'] = len(work)

    return render(request, "student/profile/profile.html", context)


def edit_student_profile(request):
    context = {}
    student = StudentInfo.objects.get(student__email=request.user.email)
    projects = Project.objects.filter(student__email=request.user.email).order_by('date_added')
    work = WorkExperience.objects.filter(student__email=request.user.email).order_by('date_added')

    total_certifications = StudentCertificate.objects.filter(student__email=request.user.email)

    tech_skills = []
    soft_skills = []
    work_points = []
    project_points = []

    if student.technical_skills:
        skills_string = student.technical_skills
        tech_skills = [skill.strip() for skill in skills_string.split(',')]

    if student.soft_skills:
        soft_skills_string = student.soft_skills
        soft_skills = [skill.strip() for skill in soft_skills_string.split(',')]

    for i in work:
        work_key_points = []

        if i.key_points:
            key_points_string = i.key_points
            key_points = [skill.strip() for skill in key_points_string.split(',')]
            work_key_points.append(key_points)

        work_points.append(work_key_points)

    for i in projects:
        project_key_points = []

        if i.key_points:
            key_points_string = i.key_points
            key_points = [skill.strip() for skill in key_points_string.split(',')]
            project_key_points.append(key_points)

        project_points.append(project_key_points)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # Get the StudentInfo object for the current user
        student_info = StudentInfo.objects.get(student__email=request.user.email)

        if form_type == 'form1':
            designation = request.POST.get('designation')
            city = request.POST.get('city')
            exp_years = request.POST.get('exp_years')

            # Update the fields and save the object
            student_info.designation = designation
            student_info.city = city
            student_info.experience_years = exp_years
            student_info.save()
            return redirect("edit_student_profile")
        elif form_type == 'form2':
            about_me = request.POST.get('about_me')
            tech_skills = request.POST.get('tech_skills')
            soft_skills = request.POST.get('soft_skills')

            # Update the fields and save the object
            student_info.about_me = about_me
            student_info.technical_skills = tech_skills
            student_info.soft_skills = soft_skills
            student_info.save()
            return redirect("edit_student_profile")
        elif form_type == 'form3':
            github_link = request.POST.get('github_link')
            linkedin_link = request.POST.get('linkedin_link')

            student_info.github = github_link
            student_info.linkedin = linkedin_link
            student_info.save()
            return redirect("edit_student_profile")
        elif form_type == 'formWork':
            organization_name = request.POST.get('organization_name')
            role = request.POST.get('role')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            key_points = request.POST.get('key_points')

            # Create a new WorkExperience object and save it
            WorkExperience.objects.create(
                student=student_info.student,
                organization_name=organization_name,
                role=role,
                start_date=start_date,
                end_date=end_date,
                key_points=key_points,
            )
            return redirect("edit_student_profile")
        elif form_type == 'formProject':
            project_name = request.POST.get('project_name')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            link = request.POST.get('link')
            key_points = request.POST.get('key_points')

            # Create a new Project object and save it
            Project.objects.create(
                student=student_info.student,
                project_name=project_name,
                start_date=start_date,
                end_date=end_date,
                link=link,
                key_points=key_points,
            )
            return redirect("edit_student_profile")

    context['student'] = student
    context['projects'] = zip(projects, project_points)
    context['work'] = zip(work, work_points)
    context['total_certifications'] = len(total_certifications)
    context['total_projects'] = len(projects)
    context['tech_skills'] = tech_skills
    context['soft_skills'] = soft_skills
    context['total_work'] = len(work)

    return render(request, "student/profile/edit_profile.html", context)


def delete_work_experience(request, work_experience_id):
    work_experience = get_object_or_404(WorkExperience, id=work_experience_id)

    # Assuming you want to delete the work experience and then redirect to a specific page
    work_experience.delete()

    # Redirect to a success page or another appropriate URL
    return redirect('edit_student_profile')


def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Assuming you want to delete the project and then redirect to a specific page
    project.delete()

    # Redirect to a success page or another appropriate URL
    return redirect('edit_student_profile')


def resume(request):
    return render(request, "student/resume.html")


def student_account_settings(request):
    context = {}

    try:
        if request.method == 'POST':
            student_info = StudentInfo.objects.get(student__email=request.user.email)
            # Save the data to the StudentInfo model
            student_info.date_of_birth = request.POST.get('date_of_birth') or student_info.date_of_birth
            student_info.city = request.POST.get('city') or student_info.city
            student_info.state = request.POST.get('state') or student_info.state
            student_info.c_degree = request.POST.get('c_degree') or student_info.c_degree
            student_info.c_department = request.POST.get('c_department') or student_info.c_department
            student_info.current_year = request.POST.get('current_year') or student_info.current_year
            student_info.current_semester = request.POST.get('current_semester') or student_info.current_semester
            student_info.cgpa = request.POST.get('cgpa') or student_info.cgpa
            student_info.ss_name = request.POST.get('ss_name') or student_info.ss_name
            student_info.ss_school_name = request.POST.get('ss_school_name')
            student_info.ss_start_year = request.POST.get('ss_start_year')
            student_info.ss_end_year = request.POST.get('ss_end_year')
            student_info.ss_marks = request.POST.get('ss_marks') or 0
            student_info.ps_name = request.POST.get('ps_name') or student_info.ps_name
            student_info.ps_school_name = request.POST.get('ps_school_name') or student_info.ps_school_name
            student_info.ps_start_year = request.POST.get('ps_start_year') or student_info.ps_start_year
            student_info.ps_end_year = request.POST.get('ps_end_year') or student_info.ps_end_year
            student_info.ps_marks = request.POST.get('ps_marks') or student_info.ps_marks
            student_info.designation = request.POST.get('designation') or student_info.designation
            student_info.experience_years = request.POST.get('experience_years') or student_info.experience_years
            student_info.about_me = request.POST.get('about_me') or student_info.about_me

            student_info.division = request.POST.get('division')
            student_info.preferred_language = request.POST.get('preferred_language')
            student_info.gender = request.POST.get('gender')

            # Save the updated information
            student_info.save()

            context["message"] = "Changes done successfully."

    except Exception as e:
        context["error"] = str(e)

    student_info = StudentInfo.objects.get(student__email=request.user.email)
    context["student"] = student_info
    return render(request, "student/student_account_settings.html", context)


def download_resume(request):
    context = {}

    student = StudentInfo.objects.get(student__email=request.user.email)

    tech_skills = []
    soft_skills = []

    if student.technical_skills:
        skills_string = student.technical_skills
        tech_skills = [skill.strip() for skill in skills_string.split(',')]

    if student.soft_skills:
        soft_skills_string = student.soft_skills
        soft_skills = [skill.strip() for skill in soft_skills_string.split(',')]

    total_skills = len(tech_skills)

    tech_skills1 = []
    tech_skills2 = []

    if total_skills > 4:
        # Calculate the sizes of the two lists
        size_tech_skills1 = total_skills // 2
        size_tech_skills2 = total_skills - size_tech_skills1

        # Split the original list into two lists
        tech_skills1 = tech_skills[:size_tech_skills1]
        tech_skills2 = tech_skills[size_tech_skills1:]

        # If the sizes are not equal, adjust the sizes
        if size_tech_skills1 > size_tech_skills2:
            tech_skills1 = tech_skills[:size_tech_skills1 - 1]
            tech_skills2 = tech_skills[size_tech_skills1 - 1:]

    context["student"] = student
    if total_skills > 4:
        context['tech_skills1'] = tech_skills1
        context['tech_skills2'] = tech_skills2
    else:
        context['tech_skills2'] = tech_skills

    context['soft_skills'] = soft_skills

    return render(request, "student/resume.html", context)


def profile_api(request, batu_prn):
    context = {}
    student = StudentInfo.objects.get(student__batu_prn=batu_prn)
    projects = Project.objects.filter(student__batu_prn=batu_prn).order_by('date_added')
    work = WorkExperience.objects.filter(student__batu_prn=batu_prn).order_by('date_added')

    total_certifications = StudentCertificate.objects.filter(student__batu_prn=batu_prn)

    tech_skills = []
    soft_skills = []
    work_points = []
    project_points = []

    if student.technical_skills:
        skills_string = student.technical_skills
        tech_skills = [skill.strip() for skill in skills_string.split(',')]

    if student.soft_skills:
        soft_skills_string = student.soft_skills
        soft_skills = [skill.strip() for skill in soft_skills_string.split(',')]

    for i in work:
        work_key_points = []

        if i.key_points:
            key_points_string = i.key_points
            key_points = [skill.strip() for skill in key_points_string.split(',')]
            work_key_points.append(key_points)

        work_points.append(work_key_points)

    for i in projects:
        project_key_points = []

        if i.key_points:
            key_points_string = i.key_points
            key_points = [skill.strip() for skill in key_points_string.split(',')]
            project_key_points.append(key_points)

        project_points.append(project_key_points)

    context['student'] = student
    context['projects'] = zip(projects, project_points)
    context['work'] = zip(work, work_points)
    context['total_certifications'] = len(total_certifications)
    context['total_projects'] = len(projects)
    context['tech_skills'] = tech_skills
    context['soft_skills'] = soft_skills
    context['total_work'] = len(work)

    return render(request, "student/profile/profile_api.html", context)