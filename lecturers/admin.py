from django.contrib import admin

from .models import Lecturer

# Register your models here.
@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "gender", "title"]
    search_fields = ["user", "gender", "title", "date_of_birth"]