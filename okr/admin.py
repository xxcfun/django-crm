from django.contrib import admin

# Register your models here.
from okr.models import Okr


@admin.register(Okr)
class OkrAdmin(admin.ModelAdmin):
    list_display = ('object', 'key1', 'key1_true', 'key2', 'key2_true',
                    'key3', 'key3_true', 'results', 'finish', 'user',
                    'created_at', 'is_valid', )
    list_per_page = 10
    ordering = ['-created_at']
