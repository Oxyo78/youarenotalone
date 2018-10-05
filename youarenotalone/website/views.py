import re
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import loginUser, createUser, MessageReply, SearchPeople, ComposeMessage, InterestAdd, InterestDel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django_messages.models import Message, inbox_count_for
from django.utils import timezone
from django.http import Http404, HttpResponse, JsonResponse
from .models import Interest, UserProfile, City, News
from django.core import serializers

def index(request):
    """ Home page render """

    # Check for modal rgpd
    if request.session.get('rgpd'):
        cookiesAccept = False
    else:
        cookiesAccept = True


    # Get the last 3 news from the database
    news = News.objects.all().order_by('id')[:3]

    # Get the number of unread message
    if request.user.is_authenticated:
        userName = request.user
        unreadMessage = inbox_count_for(userName)
        if unreadMessage == 0:
            unreadMessage = None

    # User connexion
    if request.method == "POST":
        logForm = loginUser(request.POST)
        if logForm.is_valid():
            username = logForm.cleaned_data['username']
            password = logForm.cleaned_data['password']
            authenticate_user = authenticate(username=username, password=password)
            if authenticate_user:
                login(request, authenticate_user)
                succesText = 'Bienvenue !'
                loginSuccess = True
                error = False
                userName = request.user
                unreadMessage = inbox_count_for(userName)
                if unreadMessage == 0:
                    unreadMessage = None
                searchForm = SearchPeople()
                composeForm = ComposeMessage()
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
            cityInput = subForm.cleaned_data['city']
            # Check if the input password is correct (lenght 8 and 1 number inside)
            if password == password2:
                if len(password) >= 8:
                    # Check if password contain a number
                    if bool(re.search(r'\d', password)) is True:
                        # Check if password contain a letter
                        if bool(re.search(r'[a-zA-Z]', password)) is True:
                            # check if the email form is correct
                            if bool(re.search(r'[^@]+@[^@]+\.[^@]+', email)) is True:
                                # Check if the email address doesn't already exist in database
                                if not User.objects.filter(email=email).exists():
                                    # Check if the username doesn't already exist in the database
                                    if not User.objects.filter(username=username).exists():
                                        try:
                                            cityParse = cityInput.split(" ")
                                            print(cityParse)
                                            if len(cityParse) > 2:
                                                name = str(cityParse[0]) + " " + str(cityParse[1])
                                                print("name: " + str(name))
                                                cityQuery = City.objects.filter(cityName__istartswith=name.upper())[:1]
                                                cityWord = cityQuery[0]
                                            else:
                                                cityQuery = City.objects.filter(cityName__istartswith=cityParse[0].upper())[:1]
                                                cityWord = cityQuery[0]
                                                
                                        except:
                                            errorText = "Le nom de ville entrée n'a pas été trouvé"
                                            error = True
                                            subscribeForm = createUser()
                                            loginForm = loginUser()
                                            return render(request, 'website/templates/index.html', locals())

                                        user = User.objects.create_user(username.capitalize(), email, password)
                                        user.save()
                                        user.userprofile.city = cityWord
                                        user.save()
                                        user = authenticate(username=username.capitalize(), password=password)
                                        login(request, user)
                                        succesText = 'Vous êtes connecté ! Veuillez compléter votre profil !'
                                        loginSuccess = True
                                        error = False
                                        userName = request.user
                                        composeForm = ComposeMessage()
                                        searchForm = SearchPeople()
                                        return render(request, 'website/templates/index.html', locals())
                                    else:
                                        errorText = "Nom d'utilisateur déja pris"
                                        error = True
                                        subscribeForm = createUser()
                                        loginForm = loginUser()
                                else:
                                    errorText = "Un compte utilise déjà cette email"
                                    error = True
                                    subscribeForm = createUser()
                                    loginForm = loginUser()           
                            else:
                                errorText = "L'email n'est pas valide"
                                error = True
                                subscribeForm = createUser()
                                loginForm = loginUser()           
                        else:
                            errorText = "Le mot de passe doit contenir au moins 1 lettre"
                            error = True
                            subscribeForm = createUser()
                            loginForm = loginUser()           
                    else:
                        errorText = 'Le mot de passe doit contenir au moins 1 chiffre'
                        error = True
                        subscribeForm = createUser()
                        loginForm = loginUser()           
                else:
                    errorText = 'Le mot de passe est trop court, il doit faire au minimum 8 caractères et contenir au moins 1 chiffre'
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

    composeForm = ComposeMessage()
    searchForm = SearchPeople()

    return render(request, 'website/templates/index.html', locals())


@login_required
def logoutUser(request):
    """ Logout user """
    logout(request)
    return redirect(reverse(index))


@login_required
def messageInbox(request):
    """ get the message list for the user """
    message_list = Message.objects.inbox_for(request.user)

    # Get the number of unread message
    userName = request.user
    unreadMessage = inbox_count_for(userName)
    if unreadMessage == 0:
        unreadMessage = None

    return render(request, 'website/templates/message.html', locals())


@login_required
def viewMessage(request, messageId):
    """ Return the message detail """
    user = request.user
    now = timezone.now()
    messageToView = get_object_or_404(Message, id=messageId)
    if (messageToView.sender != user) and (messageToView.recipient != user):
        raise Http404
    if messageToView.read_at is None and messageToView.recipient == user:
        messageToView.read_at = now
        messageToView.save()
    
    # Get the number of unread message
    userName = request.user
    unreadMessage = inbox_count_for(userName)
    if unreadMessage == 0:
        unreadMessage = None

    if request.method == "POST":
        bodyForm = MessageReply(request.POST)
        if bodyForm.is_valid():
            body = bodyForm.cleaned_data['body']
            try:
                msg = Message.objects.create(subject=messageToView.subject, body=body, sender=userName,
                                            recipient=messageToView.sender, parent_msg=messageToView.parent_msg, sent_at=now)
                msg.save()
                succesText = 'Message envoyé'
                loginSuccess = True
            except ValueError as e:
                print('erreur: ', e)
            message_list = Message.objects.inbox_for(request.user)
            return render(request, 'website/templates/message.html', locals())
        else:
            errorText = 'Message non envoyé'
            error = True
            bodyForm = MessageReply()
    else:
        error = False
        loginSuccess = False
        bodyForm = MessageReply()

    message_list = Message.objects.inbox_for(request.user)

    return render(request, 'website/templates/message.html', locals())


@login_required
def account(request):
    """ Account page """
    user = request.user

    # Check email unread
    unreadMessage = inbox_count_for(user)
    if unreadMessage == 0:
        unreadMessage = None

    interestList=user.userprofile.interestId.all()

    if request.method == "POST":
        addForm = InterestAdd(request.POST)
        if addForm.is_valid():
            interestSelect = addForm.cleaned_data['interestAdd']
            interestInput = addForm.cleaned_data['newInterest']
            getInterest = Interest.objects.get(id=interestSelect)
            user.userprofile.interestId.add(getInterest)
            if interestInput:
                obj, newInterest = Interest.objects.get_or_create(interestName = interestInput.capitalize())
                user.userprofile.interestId.add(obj.id)
                user.save()
                interestForm = InterestAdd()
                delForm = InterestDel(user=user)
                return render(request, 'website/templates/account.html', locals())
            else:
                interestForm = InterestAdd()
                delForm = InterestDel(user=user)
                return render(request, 'website/templates/account.html', locals())
        
        delForm = InterestDel(request.POST, user=user)
        if delForm.is_valid():
            interestDel = delForm.cleaned_data['interestDel']
            getInterest = Interest.objects.get(id=interestDel)
            user.userprofile.interestId.remove(getInterest)
            user.save()
            interestForm = InterestAdd()
            delForm = InterestDel(user=user)
            return render(request, 'website/templates/account.html', locals())
    else:
        addForm = InterestAdd()
        delForm = InterestDel(user=user)

    return render(request, 'website/templates/account.html', locals())

@login_required
def searchUsers(request):
    """ Get a list of user with same interest """
    searchInterest = request.GET.get('searchInterest')
    user = request.user
    data = {}
    try:
        userInterest = Interest.objects.get(id = searchInterest)
        userLoc = userInterest.interestUser.all()
        for item in userLoc:
            if item.user.username != user.username:
                data[item.user.username] = {}
                data[item.user.username]['name'] = item.user.username
                data[item.user.username]['Lng'] = item.city.coordinateLng
                data[item.user.username]['Lat'] = item.city.coordinateLat    
    except:
        data['noResult'] = 'No results found'
    
    if not data:
        data['noResult'] = 'No results found'

    return JsonResponse(data)


@login_required
def newMessage(request):
    """ Send a new message to the select user """
    data = {}
    recipient = request.POST.get('recipient')
    subject = request.POST.get('subject')
    body = request.POST.get('body')
    now = timezone.now()
    user = request.user
    try:
        recipientUser = User.objects.get(username=recipient)
        msg = Message.objects.create(subject=subject,
                                    body=body,
                                    sender=user,
                                    recipient_id=recipientUser.id,
                                    sent_at=now)
        msg.save()
        data['succesText'] = 'Message envoyé'
        data['loginSuccess'] = 'True'

    except ValueError as e:
        data['error'] = e
        
    return JsonResponse(data)

def legalize(request):
    """ Show the legalize page """
    user = request.user

    # Get the number of unread message
    if request.user.is_authenticated:
        userName = request.user
        unreadMessage = inbox_count_for(userName)
        if unreadMessage == 0:
            unreadMessage = None
    loginForm = loginUser()
    subscribeForm = createUser()
    return render(request, 'website/templates/legal.html', locals())

def completeCity(request):
    """Auto-complete views in Ajax for the city"""
    if request.is_ajax():
        cityEntry = request.GET.get('term')
        data = []
        cityList = City.objects.filter(cityName__istartswith=cityEntry).order_by('cityName')[:5]
        for item in cityList:
            data.append(item.cityName +" "+ str(item.postalCode))
        if not data:
            data.append("Aucun résultat")
    return JsonResponse(data, safe=False)

def acceptCookies(request):
    """ Set time for accepting cookies """
    if request.is_ajax():
        setCookieAccept = request.GET.get('setCookieAccept')
        request.session['rgpd'] = 'True'
        return redirect(reverse(index))