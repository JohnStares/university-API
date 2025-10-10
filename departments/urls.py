from django.urls import path

from . import views


urlpatterns = [
    path("add/", views.AddDepartments.as_view(), name='department'),
]