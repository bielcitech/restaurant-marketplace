from django.urls import path
from accounts.views import registerUser


urlpatterns = [
    path('register-user/', registerUser, name='register-user')
]