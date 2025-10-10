from django.urls import path


from . import views


urlpatterns = [
    path("add/", views.CourseView.as_view(), name="courses"),
]