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

def splitArrayIntoPairs(arr):
	pairs = list(itertools.combinations(arr,2))
	log.debug('\n pairs: %s',pairs)
	return pairs

def getFileViaUrl(url):
	response = requests.get(url)
	return Image.open(StringIO(response.content))
