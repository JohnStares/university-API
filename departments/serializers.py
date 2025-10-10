from rest_framework import serializers

from .models import Departments


class DepartmentSerializer(serializers.ModelSerializer):
    faculty = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

    class Meta:
        model = Departments
        fields = ["id", "faculty", "name", "date_created"]

        