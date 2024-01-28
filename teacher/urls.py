from django.conf.urls.static import static
from django.urls import path
from .views import *
from ssms import settings

urlpatterns = [
    path("", teacher_dashboard, name="teacher_dashboard"),
    path("add_student/", add_student, name="add_student"),
    path("display_student/", display_student, name="display_student"),
    path("filter_and_export/", filter_and_export, name="filter_and_export"),

    path("upload_student_excel/", upload_student_excel, name="upload_student_excel"),
    path("download_sample_file/", download_sample_file, name="download_sample_file"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)