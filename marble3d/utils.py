import json
from django.conf import settings
from PIL import Image, ImageDraw
import logging
import dropbox
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
from polygons import enlargePolygon



def publishImage(image):
	image_data = {
		'image_id' : image.id,
		'block_title' : image.block.title,
		'image_filename': image.filename,
		'url': image.url
	}
	url = settings.CROWDCAFE['api_url']+'job/'+str(image.block.job_id)+'/unit/'

	r = sendRequest('post',url,image_data)

	if r.status_code in [201,200]:
		image.status = 'NC'
		image.save()
		return image
	else:
		image.delete()
		return False

def sendRequest(request_type, url,data = {}):
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

def splitArrayIntoPairs(arr):
    return [[arr[i-1],arr[i]] for i in range(len(arr))] 


def updateUnitStatus(unit_id, status = 'NC'):
    url = settings.CROWDCAFE['api_url']+'unit/'+str(unit_id)
    log.debug('unit status update url: '+str(url))
    r = sendRequest('patch',url,{'status':status})
    log.debug('unit status update '+str(r))
    if r.status_code in [201,200]:
    	log.debug('unit status update url: '+str(r.json()))
        if r.json()['status'] == status:
            return True
    return False

def sendFileToDropbox(cropped_image_filename, folder, filename, dropbox_token, dropbox_secret):
	dropbox_path = settings.DROPBOX_FOLDER_NAME+'/'+folder+'/'+filename
	sess = session.DropboxSession(settings.DROPBOX_APP_ID, settings.DROPBOX_API_SECRET, 'dropbox')
	sess.set_token(dropbox_token,dropbox_secret)
	dropbox_client = client.DropboxClient(sess)	
	f = open(cropped_image_filename, 'rb')

	return dropbox_client.put_file(dropbox_path, f)

def getScaledPolygon(imagefile, polygon_data):
	width, height = imagefile.size
	log.debug('polygon original:'+str(polygon_data['polygon']))
	enlarged_polygon = enlargePolygon(polygon_data['polygon'],settings.MARBLE_3D_ENLARGE_POLYGON)
	log.debug('polygon enlarged:'+str(enlarged_polygon))
	return [(point['x']*width/polygon_data['canvas_size']['width'], point['y']*height/polygon_data['canvas_size']['height']) for point in enlarged_polygon]

def getFileViaUrl(url):
	response = requests.get(url)
	return Image.open(StringIO(response.content))

def cropImageViaPolygon(imagefile, polygon):
	im = imagefile.convert("RGBA")
	# read image as RGB and add alpha (transparency)
	# convert to numpy (for convenience)
	imArray = numpy.asarray(im)
	# create mask
	maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
	ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
	mask = numpy.array(maskIm)
	# assemble new image (uint8: 0-255)
	newImArray = numpy.empty(imArray.shape,dtype='uint8')
	# colors (three first columns, RGB)
	newImArray[:,:,:3] = imArray[:,:,:3]
	# transparency (4th column)
	newImArray[:,:,3] = mask*255
	# back to Image from numpy
	return Image.fromarray(newImArray, "RGBA")
