from rest_framework import serializers

from .models import Courses


class CoursesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    units = serializers.IntegerField(required=True)

    departments = serializers.CharField(required=True)
    faculty = serializers.CharField()

    class Meta:
        model = Courses
        fields = ["id", "title", "code", "units", "departments", "faculty", "date_created"]

