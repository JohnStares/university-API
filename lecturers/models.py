from django.db import models
from authentication.models import CustomUser


from departments.models import Departments

# Create your models here.
class Lecturer(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', "Female")
    )

    TITLE = (
        ('Prof', 'Professor'),
        ('Dr', 'Doctor')
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(null=False, blank=False)
    gender = models.CharField(max_length=6, choices=GENDER, null=False, blank=False)
    title = models.CharField(max_length=6, choices=TITLE)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.title} {self.user.get_full_name()}"

