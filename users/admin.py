from django.contrib import admin

from users.models import User, Count


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'password', 'is_valid', 'professional', 'role', 'created_time')
    list_per_page = 10
    ordering = ['-created_time']


@admin.register(Count)
class CountAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'day_customer', 'day_liaison', 'day_record', 'day_business',
                    'month_customer', 'month_liaison', 'month_record', 'month_business',
                    'all_customer', 'all_liaison', 'all_record', 'all_business',)
