from django.urls import path


from rest_framework_simplejwt.views import TokenRefreshView

from . import views


urlpatterns = [
    path("register/", views.StudentRegister.as_view(), name="register"),
    path("register/lecturer/", views.LecturerRegister.as_view(), name="register_lecturer"),
    path("token/refresh/", TokenRefreshView.as_view(), name='refresh'),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]