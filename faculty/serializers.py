from rest_framework import serializers

from .models import Faculties

class FacultySerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Faculties
        fields = ["id", "name", "date_created"]



