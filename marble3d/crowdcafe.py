import json
from django.conf import settings
from polygons import enlargePolygon, getPolygonArea, getPolygonCenter, getDistance, getPolygonAreaDiagonalLength, getRectangleCoordinates, getPolygonPoints, getCanvasSize
import logging
from utils import splitArrayIntoPairs, sendRequest, updateUnitStatus, getFileViaUrl, getScaledPolygon, cropImageViaPolygon, sendFileToDropbox
import random
import os
from models import Image as Img, Block

log = logging.getLogger(__name__)

# Bring judgement information from CrowdCafe into structure
class CrowdCafeJudgement:
	def __init__(self, crowdcafe_data):

		#log.debug('data: '+ str(shape_data))

		self.threashold = settings.MARBLE_3D_ERROR_THREASHOLD
		self.data = crowdcafe_data

		self.shape = self.getShapes()
		log.debug('info: '+ str(self))
	def is_exist(self):
		return 'shapes' in self.data['output_data']:
	def getShapes(self):
		judgement_shape = {}
		if self.is_exist():
			shapes = json.loads(self.data['output_data']['_shapes'])
			for shape in shapes['objects']:
				if shape['type'] == 'image':
					judgement_shape['canvas_size'] = getCanvasSize(shape)
				if shape['type'] == 'rect':
					judgement_shape['polygon'] = getRectangleCoordinates(shape)
					log.debug('rectangle points: '+ str(judgement_shape[handler]['polygon']))
				if shape['type'] == 'polygon':
					judgement_shape['polygon'] = getPolygonPoints(shape)
			return judgement_shape
		else:
			return False
	
	def cropAndSave(self, input_data, dropbox_token, dropbox_secret):
		log.debug('create a cropped image, based on the judgement'+str(self))
		# get image file from url
		imagefile = getFileViaUrl(input_data['url'])
		# bring polygon points to required tuple structure and enlarge it according to settings
		polygon = getScaledPolygon(imagefile, self.shape)
		log.debug('polygon: '+ str(polygon))
		log.debug('enlarged polygon: '+ str(polygon))
		# get cropped image by polygon
		croppedImage = cropImageViaPolygon(imagefile, polygon)
		# save this cropped image in a file
		cropped_image_filename = str(random.randint(1000000, 9999999))+'.png'
		image_path = os.path.join(settings.MEDIA_ROOT, cropped_image_filename)
		log.debug('cropped_image_filename: '+ str(cropped_image_filename))
		# save this file into dropbox
		croppedImage.save(image_path)
		uploaded = sendFileToDropbox(image_path, input_data['block_title'], input_data['image_filename']+'.png', dropbox_token, dropbox_secret)
		log.debug('uploaded to dropbox: '+ str(uploaded))

		
		try:
			os.unlink(image_path)
			log.debug('file deleted: '+ str(image_path))
		except:
			pass

# Compare pair of CrowdCafeJudgements
class Evaluation:
	def __init__(self, judgement1,judgement2, threashold):
		self.judgement1 = judgement1
		self.judgement2 = judgement2 # judgement2 is considered as gold in gold evaluation tasks
		self.threashold = threashold

		if self.judgement1.is_exist() and self.judgement2.is_exist()
		self.scale = self.getScale()

	def getScale(self):
		#TODO - do we need float here?
		scale = {
			'x' : float(self.judgement1.shape['canvas_size']['width'])/float(self.judgement2.shape['canvas_size']['width']),
			'y' : float(self.judgement1.shape['canvas_size']['height'])/float(self.judgement2.shape['canvas_size']['height'])
		}
		log.debug('scale: ' + str(scale))
		return scale

	# handle2 gold
	def judgementsAreSimilar(self):
		log.debug('\n **********************\n check judgements similarity')
		# if some of judgements are empty - return false
		if not self.judgement1.is_exist() or not self.judgement2.is_exist():
			return False
		evaluated = self.checkCentralPoint() and self.checkArea()
		
		log.debug('\n judgements are similar to each other: '+ str(evaluated)+'\n**********************')
		
		return evaluated

	def checkCentralPoint(self): 
		
		central_points = {}
		central_points['judgement1'] = getPolygonCenter(self.judgement1.shape['polygon'])
		central_points['judgement2'] = getPolygonCenter(self.judgement2.shape['polygon'])

		delta_absolute = {
			'x':abs(central_points['judgement1']['x']/self.scale['x']-central_points['judgement2']['x']),
			'y':abs(central_points['judgement1']['y']/self.scale['y']-central_points['judgement2']['y'])
		}

		log.debug('central point delta absolute: ' + str(delta_absolute))
		
		judgement2_diagonal_length = getPolygonAreaDiagonalLength(self.judgement2.shape['polygon'])
		log.debug('polygon area diagonal length: '+ str(judgement2_diagonal_length))

		delta_relative = {
			'x': delta_absolute['x']/judgement2_diagonal_length,
			'y': delta_absolute['y']/judgement2_diagonal_length
		}

		log.debug('central point delta relative: ' + str(delta_relative))

		return delta_relative['x'] < self.threashold['center_distance'] and delta_relative['y']<self.threashold['center_distance']

	def checkArea(self):
		area = self.getArea()
		return max([area['judgement1'],area['judgement2']])/min([area['judgement1'],area['judgement2']])<= self.threashold['area_max']

	def getArea(self):
		area = {}
		area['judgement1'] = getPolygonArea(self.judgement1.shape['polygon'])
		area['judgement2'] = getPolygonArea(self.judgement2.shape['polygon'])*(self.scale['x']*self.scale['y'])

		log.debug('area: ' + str(area))
		return area

def controlCrowdCafeData(data_in_json):
	judgements = {}
	for item in data_in_json:
		if item['gold']:
			judgements['gold'] = CrowdCafeJudgement(crowdcafe_data = item)
		else:
			judgements['given'] = CrowdCafeJudgement(crowdcafe_data = item)
	evaluation = Evaluation(judgement1 = judgements['given'],judgement2 = judgements['gold'],threashold = settings.MARBLE_3D_ERROR_THREASHOLD)
	return evaluation.judgementsAreSimilar()