from django.urls import path

from . import views


urlpatterns = [
    path("add/", views.FacultyView.as_view(), name="faculty"),
]