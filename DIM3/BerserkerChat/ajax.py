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



    if (data != ""):
        request.session['guest_name'] = data

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

@dajaxice_register
def getRoom(request, name, room):
    print "room :" + room
    if (name != ""):
        request.session['guest_name'] = name
    r, created = Room.objects.get_or_create(name=room, slug=room, allow_anonymous_access=True)
    print r.slug
    if (created):
        r.save()
        r = Room.objects.get(slug=room)
    c = RequestContext(request, {'user':request.user,'room': r })
    t = loader.get_template('chatrooms/room.html')
    page = t.render(c)
    print page
    return simplejson.dumps({'name': "Public(" + room + ")", 'tab':page})