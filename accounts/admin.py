from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User, UserProfile

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_filter = ()
    filter_horizontal = ()
    list_display = ('email', 'username', 'is_vendor', 'date_joined')
    ordering = ('-date_joined',)
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)