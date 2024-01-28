from django.urls import path
from .views import *

urlpatterns = [
    path("", student_dashboard, name="student_dashboard"),
    path('profile/<int:batu_prn>/', profile_api, name='profile_api'),
    path("profile/", student_profile, name="student_profile"),
    path("resume/", resume, name="resume"),
    path('download_resume/', download_resume, name='download_resume'),
    path("settings/", student_account_settings, name="student_account_settings"),
    path("edit_profile/", edit_student_profile, name="edit_student_profile"),
    path('delete/work_experience/<int:work_experience_id>/', delete_work_experience, name='delete_work_experience'),
    path('delete/project/<int:project_id>/', delete_project, name='delete_project'),

]
