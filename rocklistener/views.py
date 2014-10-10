import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from dbx import Dbx
from general.crowdcafe import CrowdCafe
from django.shortcuts import redirect, HttpResponseRedirect

import logging
log = logging.getLogger(__name__)
job_id = 8
crowdcafe = CrowdCafe()

@csrf_exempt
def webhook_dropbox(request):
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
            updates = dbuser.checkUpdates()
            log.debug(updates)
            for path, metadata in updates:
                log.debug('path and metadata')
                log.debug(path)
                
                # create unit
                rockpearl_url = 'http://rockpearl.crowdcafe.io/'
                image_url = rockpearl_url+'rocklistener/getMediaLink/'+str(uid)+'/?'+path

                filename = path[path.rfind('/')+1:len(path)]
                rest_path = path[:path.rfind('/')]
                folder = rest_path[rest_path.rfind('/')+1:len(rest_path)]
                unit_data = {
                        'image_id' : image.id,
                        'uid': uid,
                        'block_title' : folder,
                        'image_filename': filename,
                        'url': image_url
                    }
                unit = crowdcafe.createUnit(job_id, unit_data)
                log.debug(unit)
                #if crowdcafe.createUnit(job_id, unit_data) in [200,201]:
    	return HttpResponse(status=200)

def getMediaLink(request, uid):
    if uid and 'path' in request.GET:
        dbuser = Dbx(uid)
        path = request.GET['path']
        media = dbuser.getDirectLink(path)
        return redirect(media['url'])
    else:
        return HttpResponse(status=404)