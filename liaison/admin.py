from django.contrib import admin

from liaison.models import Liaison


@admin.register(Liaison)
class LiaisonAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'customer', 'job', 'injob',
                    'wx', 'qq', 'email', 'hobby', 'birthday',
                    'remarks', 'created_at', 'is_valid', 'user')
    list_per_page = 10
