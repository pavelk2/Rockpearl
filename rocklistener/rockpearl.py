from general.crowdcafe import CrowdCafe
crowdcafe = CrowdCafe()
import logging
import json

log = logging.getLogger(__name__)

class Rockpearl:
	def __init__(self, dropbox_user):
		self.dropbox_user = dropbox_user
		self.job_id = 8
		self.rockpearl_url = 'http://rockpearl.crowdcafe.io/'

	def getMediaURL(self,path):
		media = self.dropbox_user.getDirectLink(path)
		return media['url']

	def publishImage(self,path, metadata):
		if metadata and metadata['mime_type'] in ['image/jpeg','image/png']:
			uid = self.dropbox_user.uid
			log.debug('path and metadata')
			log.debug(path)
			log.debug(metadata)
			
			new_metadata = self.dropbox_user.client.metadata(path, include_media_info = True)
			log.debug(new_metadata)

			# create unit
			image_url = self.rockpearl_url+'rocklistener/getMediaLink/'+str(uid)+'/?path='+path
			filename = path[path.rfind('/')+1:len(path)]
			rest_path = path[:path.rfind('/')]
			folder = rest_path[rest_path.rfind('/')+1:len(rest_path)]

			unit_data = {
			'image_id' : 123,
			'uid': uid,
			'path':path,
			'block_title' : folder,
			'image_filename': filename,
			'url': image_url}
			unit = crowdcafe.createUnit(self.job_id, unit_data)
			log.debug(unit.json())

		return True