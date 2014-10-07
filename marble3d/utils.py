import json
from django.conf import settings
from PIL import Image, ImageDraw
import logging

import requests
from django.conf import settings
from dropbox import client, session
from StringIO import StringIO
import numpy
import random
log = logging.getLogger(__name__)
from models import Image as Img, Block
import os
import json
import itertools


def sendFileToDropbox(image, folder, filename, dropbox_token, dropbox_secret):
	dropbox_path = settings.DROPBOX_FOLDER_NAME+'/'+folder+'/'+filename

	sess = session.DropboxSession(settings.DROPBOX_APP_ID, settings.DROPBOX_API_SECRET, 'dropbox')
	sess.set_token(dropbox_token,dropbox_secret)
	dropbox_client = client.DropboxClient(sess)	

	buffer = StringIO()
	image.save(buffer, "JPEG")
	return dropbox_client.put_file(dropbox_path, buffer)

class CrowdCafeCall:
	def publishImage(self,image):
		image_data = {
			'image_id' : image.id,
			'block_title' : image.block.title,
			'image_filename': image.filename,
			'url': image.url
		}
		url = settings.CROWDCAFE['api_url']+'job/'+str(image.block.job_id)+'/unit/'

		r = self.sendRequest('post',url,image_data)

		if r.status_code in [201,200]:
			image.status = 'NC'
			image.save()
			return image
		else:
			image.delete()
			return False

	def sendRequest(self,request_type, url,data = {}):
		headers = {
			'Content-type': 'application/json',
			'Authorization':'Token '+settings.CROWDCAFE['user_token']+'|'+settings.CROWDCAFE['app_token']
		}
		r = False
		if request_type == 'post':
			r = requests.post(url, data = json.dumps(data), headers = headers)
		elif request_type == 'get':
			r = requests.get(url, headers = headers)
		elif request_type == 'patch':
			r = requests.patch(url, data = json.dumps(data), headers = headers)
		return r

	def updateUnitStatus(unit_id, status):
		url = settings.CROWDCAFE['api_url']+'unit/'+str(unit_id)+'/'
		
		log.debug('unit status update url: '+str(url))
		
		r = self.sendRequest('patch',url,{'status':status})
		
		log.debug('unit status update '+str(r))
		
		if r.status_code in [201,200]:
			log.debug('unit status update url: '+str(r.json()))
			if r.json()['status'] == status:
				return True
		return False

def splitArrayIntoPairs(arr):
	pairs = list(itertools.combinations(arr,2))
	log.debug('\n pairs: %s',pairs)
	return pairs

def getFileViaUrl(url):
	response = requests.get(url)
	return Image.open(StringIO(response.content))
