from django.contrib import admin

# Register your models here.
from business.models import Business


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer', 'winning_rate', 'money', 'remarks', 'user',
                    'created_at', 'updated_at', 'is_valid')
    list_per_page = 10
