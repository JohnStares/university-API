from django.db import models


from faculty.models import Faculties

# Create your models here.
class Departments(models.Model):
    faculty = models.ForeignKey(Faculties, related_name="department_faculty", on_delete=models.CASCADE)
    name = models.CharField(max_length=25, unique=True, null=False, blank=False)
    date_created = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"Department of {self.name} in Faculty of {self.faculty.name}"
