from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from BerserkerChat.models import UserProfile
from BerserkerChat.models import UserForm, UserProfileForm
from django.http import HttpResponse
from django.shortcuts import render_to_response
from DIM3.settings import MEDIA_ROOT

def index(request):
    # select the appropriate template to use
    template = loader.get_template('BerserkerChat/index.html')
    # create and define the context. We don't have any context at the moment
    # but later on we will be putting data in the context which the template engine
    # will use when it renders the template into a page.
    context = RequestContext(request, {})
    # render the template using the provided context and return as http response.
    return HttpResponse(template.render(context))

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