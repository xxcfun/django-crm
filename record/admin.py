from django.contrib import admin

# Register your models here.
from record.models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('theme', 'customer', 'status', 'user', 'main', 'next', 'remarks',
                    'created_at', 'updated_at', 'is_valid')
    list_per_page = 10
