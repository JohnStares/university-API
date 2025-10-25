from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.StudentProfileView.as_view(), name="student_profile"),
]