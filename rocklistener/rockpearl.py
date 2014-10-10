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
		filename = path[path.rfind('/')+1:len(path)]
		rest_path = path[:path.rfind('/')]
		folder = rest_path[rest_path.rfind('/')+1:len(rest_path)]

		if metadata and metadata['mime_type'] in ['image/jpeg','image/png'] and 'inprogress_' not in filename and 'completed_' not in filename:
			uid = self.dropbox_user.uid
			log.debug('path and metadata')
			log.debug(path)
			log.debug(metadata)
			
			new_metadata = self.dropbox_user.client.metadata(path, include_media_info = True)
			log.debug(new_metadata)

			# create unit
			
			image_data = {
			'uid': uid
			}
			unit = crowdcafe.createUnit(self.job_id, image_data)
			unit_data = unit.json()
			log.debug(unit_data)

			new_filename = '/inprogress_'+str(unit_data['pk'])+'_'+filename
			new_path = rest_path+new_filename
			rename = self.dropbox_user.client.file_move(path,new_path)

			image_url = self.rockpearl_url+'rocklistener/getMediaLink/'+str(uid)+'/?path='+new_path
			
			image_data = {
			'uid': uid,
			'path':new_path,
			'block_title' : folder,
			'image_filename': new_filename,
			'url': image_url
			}
			crowdcafe.updateUnit(unit_data['pk'],{'input_data':image_data})
		return True