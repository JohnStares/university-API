from django.contrib import admin

from .models import Courses

# Register your models here.
@admin.register(Courses)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "code", "units", "departments", "faculty"]
    search_fields = ["title", "code", "faculty", "departments"]
