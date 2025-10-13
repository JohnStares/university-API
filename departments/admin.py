from django.contrib import admin

from .models import Departments

# Register your models here.
@admin.register(Departments)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "faculty"]
    search_fields = ["name", "faculty"]