from django.contrib import admin
from vendors.models import Vendor

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    list_display_links = ('user', 'name')


admin.site.register(Vendor, VendorAdmin)