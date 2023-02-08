from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.forms import UserForm
from django.contrib import messages

# Create your views here.
def registerUser(request):
    if request.method == 'POST':
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