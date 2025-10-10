from django.db import models

from departments.models import Departments
from faculty.models import Faculties

# Create your models here.
class Courses(models.Model):
    title = models.CharField(max_length=30, null=False, blank=False, unique=True)
    code = models.CharField(max_length=10, null=False, blank=False, unique=True)
    units = models.IntegerField(null=False, blank=False)
    date_created = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    departments = models.ForeignKey(Departments, related_name="departmental_courses", on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculties, related_name="faculty_courses", on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self) -> str:
        return f"{self.code} - {self.title}" 