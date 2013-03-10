from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def getTabContent(request):
    return simplejson.dumps({'tabContent':'This text was passed from ajax.py'})