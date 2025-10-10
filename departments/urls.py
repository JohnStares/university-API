from django.urls import path

from . import views


urlpatterns = [
    path("add/", views.DepartmentsView.as_view(), name='department'),
]