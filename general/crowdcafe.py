import json
import requests

from django.conf import settings

# class to interact with CrowdCafe via API
class CrowdCafe:
	def __init__(self):

		self.user_token = settings.CROWDCAFE['user_token']
		self.app_token = settings.CROWDCAFE['app_token']
	
	def sendRequest(self, request_type, url,data = {}):

		reques_url = settings.CROWDCAFE['api_url'] + url
		headers = {
			'Content-type': 'application/json',
			'Authorization':'Token '+self.user_token+'|'+self.app_token
		}
		r = False
		if request_type == 'post':
			r = requests.post(reques_url, data = json.dumps(data), headers = headers)
		elif request_type == 'get':
			r = requests.get(reques_url, headers = headers)
		elif request_type == 'patch':
			r = requests.patch(reques_url, data = json.dumps(data), headers = headers)
		return r

	# Units
	def getUnit(self, unit_id):
		url = 'unit/'+str(unit_id)+'/'
		r = self.sendRequest('get',url)
		unit_data = r.json()
		
		return unit_data

	def createUnit(self,job_id, data):
		url = 'job/'+str(job_id)+'/unit/'
		r = self.sendRequest('post', url, data)
		return r.status_code

	def updateUnit(self, unit_id, data_to_update):
		url = 'unit/'+str(unit_id)+'/'
		r = self.sendRequest('patch',url, data_to_update)
		
		return r.status_code

	def listJudgements(self, unit_id):
		url = 'unit/'+str(unit_id)+'/judgement/'
		r = self.sendRequest('get',url)
		judgement_data = r.json()
		
		return judgement_data