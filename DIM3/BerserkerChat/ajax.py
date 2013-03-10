from django.template import Context, loader, RequestContext
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from chatrooms.models import Room
from django.shortcuts import render
import random, string
from chatrooms.utils.decorators import room_check_access
from chatrooms import views


@dajaxice_register
def getTabContent(request):
    rooms = Room.objects.all()
    new_slug = ''.join(random.choice(string.ascii_lowercase) for x in range(2))+str(rooms.count()),
    r = Room(name=request.user.username+" "+str(rooms.count()), slug=new_slug, allow_anonymous_access=True)
    r.save()


    r = Room.objects.get(slug=new_slug)
    t = loader.get_template('chatrooms/room.html')
    c = RequestContext(request, {'user':request.user,'room': r })
    page = t.render(c)


    return simplejson.dumps({'name': 'New Tab', 'tab':page})
