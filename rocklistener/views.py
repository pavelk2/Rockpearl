import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from dbx import Dbx

from django.shortcuts import redirect, HttpResponseRedirect
from rockpearl import Rockpearl
import logging

log = logging.getLogger(__name__)

@csrf_exempt
def webhook_dropbox(request):
    if 'challenge' in request.GET:
    	return HttpResponse(request.GET['challenge'])
    else:
    	for uid in json.loads(request.body)['delta']['users']:

            dbuser = Dbx(uid)
            updates = dbuser.checkUpdates()
            log.debug(updates)
            
            for update  in updates:
                rockpearl = Rockpearl(dbuser)
                rockpearl.publishImage(update)
    	
        return HttpResponse(status=200)

def getMediaLink(request, uid):
    if uid and 'path' in request.GET:

        dbuser = Dbx(uid)
        rockpearl = Rockpearl(dbuser)
        
        return redirect(rockpearl.getMediaURL(path))
    else:
        return HttpResponse(status=404)