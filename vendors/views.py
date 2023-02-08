from django.shortcuts import render, redirect
from accounts.forms import UserForm
from accounts.models import UserProfile
from vendors.forms import VendorForm
from django.contrib import messages

# Create your views here.
def registerVendor(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            # Register the user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_vendor = True
            user.save()
            # Register the vendor
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = UserProfile.objects.get(user=user)
            vendor.save()
            messages.success(request, "Votre inscription est effectuée avec succès, veuillez attendre que l'admin valide votre inscription.")
            return redirect('register-vendor')
        else:
            messages.error(request, "Votre formulaire contient des erreurs.")
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form': form,
        'v_form': v_form
    }
    return render(request, 'vendors/register_vendor.html', context)