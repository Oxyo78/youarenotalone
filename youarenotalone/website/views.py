from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import loginUser, createUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models.query import QuerySet


def index(request):
    """ Home page render """
    error = False
    errorText = ''

    # Get the username
    userName = request.user

    # User connexion
    if request.method == "POST":
        logForm = loginUser(request.POST)
        if logForm.is_valid():
            username = logForm.cleaned_data['username']
            password = logForm.cleaned_data['password']
            authenticate_user = authenticate(username=username, password=password)
            if authenticate_user:
                login(request, authenticate_user)
                loginSuccess = True
                error = False
                return render(request, 'website/templates/index.html', locals())
            else:
                errorText = 'Utilisateur inconnu ou mauvais de mot de passe'
                error = True
                loginForm = loginUser()
                subscribeForm = createUser()
        
        # User subscribe modal
        subForm = createUser(request.POST)
        if subForm.is_valid():
            username = subForm.cleaned_data['username']
            email = subForm.cleaned_data['email']
            password = subForm.cleaned_data['password']
            password2 = subForm.cleaned_data['password2']
            # Check if the input password is correct
            if password == password2:
                # Check if the username doesn't already exist in the database
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    loginSuccess = True
                    error = False
                    return render(request, 'website/templates/index.html', locals())
                else:
                    errorText = "Nom d'utilisateur déja pris"
                    error = True
                    subscribeForm = createUser()
                    loginForm = loginUser()
            else:
                errorText = 'Les mots de passe ne correspondent pas'
                error = True
                subscribeForm = createUser()
                loginForm = loginUser()
    else:
        error = False
        loginSuccess = False
        loginForm = loginUser()
        subscribeForm = createUser()


    return render(request, 'website/templates/index.html', locals())


@login_required
def logoutUser(request):
    """ Logout user """
    logout(request)
    return redirect(reverse(index))