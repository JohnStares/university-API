from django.db import models
from authentication.models import CustomUser

# Create your models here.
class Student(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', "Female")
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    mat_no = models.CharField(max_length=13, null=True, blank=True)
    date_of_birth = models.DateField(null=False, blank=False)
    gender = models.CharField(max_length=6, choices=GENDER)


    def __str__(self):
        return f"{self.mat_no} {self.user.get_full_name()}"
    
