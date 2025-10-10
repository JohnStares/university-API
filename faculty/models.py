from django.db import models

# Create your models here.
class Faculties(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False, blank=False)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    