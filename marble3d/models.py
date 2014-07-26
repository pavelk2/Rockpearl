from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
STATUS_CHOISE = (('RM', 'Removed'), ('NP','Not published'), ('NC', 'Not completed'), ('CD', 'Completed'))

class Block(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=255, default='New Block')
	job_id = models.IntegerField(default = 25)

class Image(models.Model):
	block = models.ForeignKey(Block)
	url = models.URLField(null = True, blank = True)
	filename = models.CharField(max_length=256, null = True, blank = True)
	status = models.CharField(max_length=2, choices=STATUS_CHOISE, default='NP')
	crowdcafe_unit_id = models.IntegerField(null = True, blank = True)
	date_created = models.DateTimeField(auto_now_add=True, auto_now=False)

	@property
	def crowdcafeUnitUrl(self):
		url = settings.CROWDCAFE['base_url']
		if self.crowdcafe_unit_id:
			url+='units/'+str(self.crowdcafe_unit_id)+'/judgements/'
		else:
			url+='jobs/'+str(self.block.job_id)+'/units/'
		return url