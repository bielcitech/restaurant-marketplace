from django.urls import path
from vendors.views import registerVendor

urlpatterns = [
    path('register-vendor/', registerVendor, name='register-vendor')
]