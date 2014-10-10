import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from dbx import Dbx
from general.crowdcafe import CrowdCafe

import logging
log = logging.getLogger(__name__)

crowdcafe = CrowdCafe()
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
            updates = dbuser.checkUpdates()
            for path, metadata in updates:
                log.debug('path and metadata')
                log.debug(path)
                log.debug(dbuser.getDirectLink('/Apps/CrowdCrop'+path))
                log.debug(metadata)
                #if crowdcafe.createUnit(job_id, unit_data) in [200,201]:
    	return HttpResponse(status=200)