from django.urls import path
from accounts.views import registerUser, login, logout, dashboard, myAccount, activate, forgotPassword, resetPasswordValidate, resetPassword


urlpatterns = [
    path('register-user/', registerUser, name='register-user'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('my-account/', myAccount, name='my-account'),

    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('forgot-password/', forgotPassword, name='forgot-password'),
    path('reset-password-validate/<uidb64>/<token>/', resetPasswordValidate, name='reset-password-validate'),
    path('reset-password', resetPassword, name='reset-password')
]