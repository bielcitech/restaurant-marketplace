from django.shortcuts import render, redirect

from accounts.forms import UserForm
from accounts.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.utils import detect_user, customer_access, vendor_access, send_verification_email, get_user_by_uid
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

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

            #Send verification email
            mail_subject = 'Activation du compte'
            email_template = "accounts/emails/verification_email.html"
            send_verification_email(request, user, mail_subject, email_template)
            
            messages.success(request, "Votre inscription est effectuée avec succès. Veuillez confirmer votre inscription à travers l'email qui vous a été envoyé.")
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


def activate(request, uidb64, token):
    user = get_user_by_uid(uidb64)
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Félicitaions, votre compte est maintenant actif.')
        return redirect(detect_user(user))
    else:
        messages.error(request, "Le lien d'activation est invalide")
        return redirect(detect_user(user))


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        # On vérifie si l'email existe
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            mail_subject = 'Réinitialisation du mot de passe'
            email_template = "accounts/emails/verification_password.html"
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, "Nous vous avons envoyé un lien dans votre mail pour réinitialiser le mot de passe.")
            return redirect('login')
        
        else:
            messages.error(request, "Cet email n'existe pas dans la base de données.")
            return redirect('forgot-password')

    return render(request, "accounts/emails/forgot_password.html")


def resetPasswordValidate(request, uidb64, token):
    user = get_user_by_uid(uidb64)
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = user.pk
        messages.success(request, "S'il vous plait, réinitialiser votre mot de passe")
        return redirect('reset-password')
    else:
        messages.error(request, "Le lien a expiré.")
        return redirect(detect_user(user))


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Mot de passe réinitialisé avec succès.')
            return redirect('login')
        else:
            messages.error(request, 'Mots de passe non identiques.')
            return redirect('reset-password')
    return render(request, 'accounts/emails/reset_password.html')