"""
Celery tasks
"""
import os
from celery import Celery,task, shared_task
from social_auth.models import UserSocialAuth
from django.conf import settings
import json
from crowdcafe import CrowdCafeJudgement, Evaluation
from utils import splitArrayIntoPairs, sendRequest, updateUnitStatus
import logging
from social_auth.models import UserSocialAuth
from models import Image
log = logging.getLogger(__name__)

app = Celery('tasks', broker=settings.BROKER_URL)

@app.task()
def processCrowdCafeResult(item):
	unit_url = settings.CROWDCAFE['api_url']+'unit/'+str(item['unit'])+'/'
	#TODO - to fix - i use 'patch', because 'get' does not work
	unit = sendRequest('patch',unit_url).json()
	log.debug('unit: ' + str(unit))

	url = settings.CROWDCAFE['api_url']+'unit/'+str(item['unit'])+'/judgement/'
	judgements_of_unit = sendRequest('get',url).json()
	log.debug('judgements in the unit: ' + str(judgements_of_unit))
	
	if judgements_of_unit['count'] >= 2 and not unit['gold']:
		judgement_to_pick = getGoodJudgement(judgements_of_unit['results'])
		if not judgement_to_pick:
			# if we don't have judgements which are close to each other we update Unit status = 'Not completed'
			updateUnitStatus(item['unit'],'NC')
		else:
			processGoodJudgement(judgement_to_pick, unit)
	else:
		log.debug('judgements in the unit are less than 2')

def getGoodJudgement(unit_judgements):
	judgement_to_pick = False
	# split judgements of the unit in pairs
	for pair in splitArrayIntoPairs(unit_judgements):
		judgement1 = CrowdCafeJudgement(crowdcafe_data = pair[0])
		judgement2 = CrowdCafeJudgement(crowdcafe_data = pair[1])
		# we check if judgements in the pair are similar to each other
		evaluation = Evaluation(judgement1 = judgement1, judgement2 = judgement2, threashold = settings.MARBLE_3D_ERROR_THREASHOLD)
		if evaluation.judgementsAreSimilar():
			# if they are similar, we pick the first judgement from the pair
			judgement_to_pick = judgement1
	return judgement_to_pick

def processGoodJudgement(judgement_to_pick, unit):
	# get image to which this judgement belongs
	img_query = Image.objects.filter(pk = unit['input_data']['image_id'])
	if img_query.count()==1:
		img = img_query.get()
		# get user created the block in which this image is
		user = img.block.user
		# get dropbox credentials to send this image to dropbox of the user
		social_user = UserSocialAuth.objects.get(user=user)
		secret = social_user.tokens['access_token'].split('&')[0].split('=')[1]
		token = social_user.tokens['access_token'].split('&')[1].split('=')[1]
		# create cropped image based on the selected judgement and send to dropbox
		judgement_to_pick.cropAndSave(unit['input_data'],token,secret)
		# update image in Rockpearl
		img.status = 'CD'
		img.crowdcafe_unit_id = item['unit']
		img.save()
		# update unit in CrowdCafe
		updateUnitStatus(item['unit'],'CD')
	else:
		log.debug('image with id:' + str(unit['input_data']['image_id'])+', does not exist. We did nothing.')