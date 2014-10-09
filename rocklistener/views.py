import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from dbx import Dbx

@csrf_exempt
def webhook(request):
    '''Respond to the webhook verification (GET request) by echoing back the challenge parameter.'''
    if 'challenge' in request.GET:
    	return HttpResponse(request.GET['challenge'])
    else:
    	for uid in json.loads(request.body)['delta']['users']:
	        # We need to respond quickly to the webhook request, so we do the
	        # actual work in a separate thread. For more robustness, it's a
	        # good idea to add the work to a reliable queue and process the queue
	        # in a worker process.
            dbuser = Dbx(uid)
            dbuser.checkUpdates()
    	return HttpResponse(status=200)