from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE_CHOICE = (
        ('student', "Student"),
        ('lecturer', 'Lecturer')
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICE)
    email = models.EmailField(max_length=50, unique=True, null=False, blank=False)


    def is_student(self):
        return self.user_type == "student"
    
    def is_lecturer(self):
        return self.user_type == "lecturer"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    