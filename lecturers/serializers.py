from rest_framework import serializers

from .models import Lecturer
from students.models import Student
from authentication.models import CustomUser
from courses.models import Courses

class LecturerProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    username = serializers.CharField(source="user.username")
    department = serializers.StringRelatedField()

    class Meta:
        model = Lecturer
        fields = ["first_name", "last_name", "username", "email", "department", "date_of_birth", "title", "gender"]


class StudentUseProfile(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name", "email", "username"]


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ["id", "title", "code"]


class StudentProfileSerializer(serializers.ModelSerializer):
    user = StudentUseProfile()
    courses = CoursesSerializer(many=True)
    class Meta:
        model = Student
        fields = "__all__"