from django.contrib import admin

from .models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "user_type"]
    search_fields = ["first_name", "last_name", "email", "user_type"]
