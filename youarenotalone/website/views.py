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

    # User connexion
    if request.method == "POST":
        form = loginUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            authenticate_user = authenticate(username=username, password=password)
            if authenticate_user:
                login(request, authenticate_user)
                return redirect(reverse(index))
            else:
                error = True
                loginForm = loginUser()
    else:
        loginForm = loginUser()
        error = False

    return render(request, 'website/templates/index.html', locals())


def subscribe(request):
    """ Create User account """
    errorUsername = False
    errorPassword = False
    errorForm = False

    if request.method == "POST":
        form = createUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            # Check if the input password is correct
            if password == password2:
                # Check if the username doesn't already exist in the database
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect(reverse(index))
                else:
                    errorUsername = True
            else:
                errorPassword = True
        else:
            errorForm = True
    else:
        form = createUser()
    return render(request, 'subscribe.html', locals())


@login_required
def logoutUser(request):
    """ Logout user """
    logout(request)
    return redirect(reverse(index))