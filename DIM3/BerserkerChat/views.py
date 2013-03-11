from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from BerserkerChat.models import UserProfile
from BerserkerChat.models import UserForm, UserProfileForm, loginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from DIM3.settings import MEDIA_ROOT
from chatrooms.models import Room
import string, random

def index(request):
    HOSTNAME =  request.get_host() + "/"
    roomname = request.path
    if (roomname == "/"):
        roomname = "room"
    else:
        roomname = roomname.rsplit('/', 1)[1]
    loggedin = False
    print roomname
    invalidAttempt = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to index page.
                return HttpResponseRedirect("/")
            else:
                # Return a 'disabled account' error message
                return HttpResponse("You're account is disabled.")
        else:
            # Return an 'invalid login' error message.
            invalidAttempt = True
            print  "Invalid Password or Username " + username + " Does not exist"
            return render(request, 'BerserkerChat/index.html', {'room': Room.objects.get(slug=roomname.rsplit('/', 1)[1]), 'ROOMNAME': roomname, 'user': request.user, 'host': HOSTNAME, 'loggedin': loggedin, 'invalidAttempt': invalidAttempt })
    elif request.user.is_authenticated():
        loggedin = True

    return render(request, 'BerserkerChat/index.html', {'room': Room.objects.get(slug=roomname), 'ROOMNAME': "BerserkerChat/chat/room/"+roomname, 'user': request.user, 'host': HOSTNAME, 'loggedin': loggedin, 'invalidAttempt': invalidAttempt })


def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        uform = UserForm(data = request.POST)
        if uform.is_valid():
            user = uform.save()
            # form brings back a plain text string, not an encrypted password
            pw = user.password
            # thus we need to use set password to encrypt the password string
            user.set_password(pw)
            user.save()
            registered = True
        else:
            print uform.errors
    else:
        uform = UserForm()

    return render_to_response('BerserkerChat/register.html', {'loggedin': request.user.is_authenticated(), 'uform': uform, 'registered': registered }, context)


def save_file(file, path=''):
    filename = file._get_name()
    fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb' )
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()

@login_required
def user_logout(request):
    context=RequestContext(request)
    logout(request)


def Categories(request):
    return render(request, 'chatrooms/Categories.html')

def Recent(request):
    return render(request, 'chatrooms/Recent.html')
