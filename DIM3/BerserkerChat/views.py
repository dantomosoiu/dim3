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

def index(request):
    context = RequestContext(request)
    loggedin = False
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
            #return render_to_response('BerserkerChat/index.html', {}, context)
            return render(request, 'BerserkerChat/index.html', {'loggedin': loggedin, 'invalidAttempt': invalidAttempt })
    elif request.user.is_authenticated():
        print "here"
        loggedin = True

    return render(request, 'BerserkerChat/index.html', {'loggedin': loggedin, 'invalidAttempt': invalidAttempt })


def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        uform = UserForm(data = request.POST)
        pform = UserProfileForm(data = request.POST)
        if uform.is_valid() and pform.is_valid():
            user = uform.save()
            # form brings back a plain text string, not an encrypted password
            pw = user.password
            # thus we need to use set password to encrypt the password string
            user.set_password(pw)
            user.save()
            profile = pform.save(commit = False)
            profile.user = user
            profile.save()
            save_file(request.FILES['picture'])
            registered = True
        else:
            print uform.errors, pform.errors
    else:
        uform = UserForm()
        pform = UserProfileForm()

    return render_to_response('BerserkerChat/register.html', {'uform': uform, 'pform': pform, 'registered': registered }, context)


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

def private_link(request):
    r = Room()