from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.LecturerProfile.as_view(), name="lecturer_profile"),
    path("students/", views.StudentsProfile.as_view(), name="students"),
    path("student/<int:id>/", views.StudentProfile.as_view(), name="student"),
]