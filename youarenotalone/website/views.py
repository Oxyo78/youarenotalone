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
    error = False
    errorText = ''
    succesText = ''

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
            # Check if the input password is correct
            if password == password2:
                # Check if the username doesn't already exist in the database
                if not User.objects.filter(username=username).exists():
                    city = City.objects.get(id=cityInput)
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    user.userprofile.city = city
                    user.save()
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    succesText = 'Vous êtes connecté ! Veuillez compléter votre profil !'
                    loginSuccess = True
                    error = False
                    userName = request.user
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
            obj, newInterest = Interest.objects.get_or_create(interestName = interestInput.capitalize())
            user.userprofile.interestId.add(obj.id)
            user.save()
            interestForm = InterestAdd()
            delForm = InterestDel()
            return render(request, 'website/templates/account.html', locals())
        
        delForm = InterestDel(request.POST)
        if delForm.is_valid():
            interestDel = delForm.cleaned_data['interestDel']
            getInterest = Interest.objects.get(id=interestDel)
            user.userprofile.interestId.remove(getInterest)
            user.save()
            interestForm = InterestAdd()
            delForm = InterestDel()
            return render(request, 'website/templates/account.html', locals())
    else:
        addForm = InterestAdd()
        delForm = InterestDel()

    return render(request, 'website/templates/account.html', locals())

@login_required
def searchUsers(request):
    """ Get a list of user with same interest """
    searchInterest = request.GET.get('searchInterest')
    print("search: " +searchInterest)
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

    print("data: "+str(data))
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
        print("data: "+str(data))

    except ValueError as e:
        print('erreur: ', e)
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

    return render(request, 'website/templates/legal.html', locals())