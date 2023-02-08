from django.urls import path
from accounts.views import registerUser, login, logout, dashboard, myAccount


urlpatterns = [
    path('register-user/', registerUser, name='register-user'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('my-account/', myAccount, name='my-account'),
]