from django.template import Context, loader, RequestContext
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from chatrooms.models import Room
from django.shortcuts import render
import random, string
from chatrooms.utils.decorators import room_check_access
from chatrooms import views


@dajaxice_register
def getPrivateRoom(request, data):



    if (data != "") request.session['guest_name'] = data

    rooms = Room.objects.all()
    new_slug = ''.join(random.choice(string.ascii_lowercase) for x in range(2))+str(rooms.count())

    if(data != "") :
        r = Room(name=data+" "+str(rooms.count()), slug=new_slug, allow_anonymous_access=True)
    else:
        r = Room(name=request.user.username+" "+str(rooms.count()), slug=new_slug, allow_anonymous_access=True)

    r.save()


    r = Room.objects.get(slug=new_slug)
    t = loader.get_template('chatrooms/room.html')


    if(data != "") :
        c = RequestContext(request, {'user':data,'room': r })
    else:
        c = RequestContext(request, {'user':request.user,'room': r })



    page = t.render(c)


    return simplejson.dumps({'name': "Private(" + r.slug + ")", 'tab':page})

def getRoom(request, data):
    if (data.name != ""):
        request.session['guest_name'] = data.name
    roomname=data.slug
    r = Room.objects.get_or_create(name=roomname, slug=roomname, allow_anonymous_access=True)
    c = RequestContext(request, {'user':request.user,'room': r })
    t = loader.get_template('chatrooms/room.html')
    page = t.render(c)
    return simplejson.dumps({'name': "Public(" + roomname + ")", 'tab':page})