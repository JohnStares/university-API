from django.contrib import admin

from .models import Faculties

# Register your models here.
@admin.register(Faculties)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]