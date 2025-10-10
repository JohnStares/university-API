from django.urls import path

from . import views


urlpatterns = [
    path("add/", views.AddFaculty.as_view(), name="faculty"),
]