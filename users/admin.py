from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'password', 'is_valid', 'professional', 'role', 'created_time')
    list_per_page = 10
    ordering = ['-created_time']
