from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.forms import UserForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.utils import detect_user, customer_access, vendor_access


# Create your views here.
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "Vous êtes déjà connectés.")
        return redirect(detect_user(request.user))
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Votre inscription est effectuée avec succès.")
            return redirect('register-user')
        messages.error(request, "L'inscription a échoué, votre formulaire contient des erreurs.")
    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request, "accounts/register_user.html", context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "Vous êtes déjà connectés.")
        return redirect(detect_user(request.user))
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Vous êtes maintenant connectés.")
            return redirect(detect_user(request.user))
        else:
            messages.error(request, "La connexion a échoué")
            return redirect("login")  
    return render(request, "accounts/login.html")


def logout(request):
    auth.logout(request)
    messages.info(request, "Vous vous être déconnectés.")
    return redirect('login')


@login_required(login_url='login')
@user_passes_test(customer_access)
def myAccount(request):
    return render(request, "accounts/my_account.html")


@login_required(login_url='login')
@user_passes_test(vendor_access)
def dashboard(request):
    return render(request, "accounts/dashboard.html")