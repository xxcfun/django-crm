from django.contrib import admin

from users.models import User, Count


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'password', 'is_valid', 'professional', 'role', 'created_time')
    list_per_page = 10
    ordering = ['-created_time']


@admin.register(Count)
class CountAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name',
                    'yesterday_record', 'yesterday_phone', 'new_customer', 'new_business',
                    'week_record', 'week_phone', 'week_business',
                    'month_customer', 'follow_business', 'finish_business',)
