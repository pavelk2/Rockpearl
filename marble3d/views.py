from django.shortcuts import get_object_or_404, render_to_response, redirect, HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse
from models import Block, Image
from forms import BlockForm, ImageForm

from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from utils import publishImage
import json
from crowdcafe import CrowdCafeJudgement, Evaluation, controlCrowdCafeData
from tasks import processCrowdCafeResult
from utils import CrowdCafeCall
def home(request):
	return render_to_response('marble3d/home.html', context_instance=RequestContext(request)) 

class BlockCreateView(CreateView):
	model = Block
	template_name = "crispy.html"
	form_class = BlockForm

	def get_initial(self):
		initial = {}
		initial['user'] = self.request.user
		return initial
	
	def form_invalid(self, form):
		print form.errors
		return CreateView.form_invalid(self, form)

	def form_valid(self, form):
		block = form.save()
		block.save()

		return redirect(reverse('marble3d-home'))

class BlockUpdateView(UpdateView):
	model = Block
	template_name = "crispy.html"
	form_class = BlockForm

	def form_invalid(self, form):
		return UpdateView.form_invalid(self, form)
	def get_object(self):
		return get_object_or_404(Block, pk = self.kwargs.get('block_pk', None), user = self.request.user)
   	def form_valid(self, form):
		block = form.save()
		return redirect(reverse('marble3d-home'))

class BlockListView(ListView):
	model = Block
	template_name = "marble3d/block_list.html"

	def get_queryset(self):
		return Block.objects.filter(user = self.request.user).order_by('-id')
	def get_context_data(self, **kwargs):
		context = super(BlockListView, self).get_context_data(**kwargs)
		return context

class ImageListView(ListView):
	model = Image
	template_name = "marble3d/image_list.html"

	def get_queryset(self):
		block = get_object_or_404(Block, pk = self.kwargs.get('block_pk', None), user = self.request.user)
		return Image.objects.filter(block = block).order_by('-id')
	def get_context_data(self, **kwargs):
		context = super(ImageListView, self).get_context_data(**kwargs)
		context['imageblock'] = get_object_or_404(Block, pk = self.kwargs.get('block_pk', None),user = self.request.user)
		return context

class ImageUpdateView(UpdateView):
	model = Image
	template_name = "crispy.html"
	form_class = ImageForm

	def form_invalid(self, form):
		return UpdateView.form_invalid(self, form)
	def get_object(self):
		return get_object_or_404(Image, pk = self.kwargs.get('image_pk', None), block__user = self.request.user)
   	def form_valid(self, form):
		image = form.save()
		return redirect(reverse('marble3d-image-list', kwargs={'block_pk': image.block.id}))

def uploadImage(request, block_pk):
	call = CrowdCafeCall()
	block = get_object_or_404(Block, pk = block_pk)
	
	image = Image(block = block, filename = request.POST['filename'], url = request.POST['image_url'])
	image.save()
	if call.publishImage(image):
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=500)

@csrf_exempt
def controlJudgement(request):
	data = json.loads(request.body)
	if controlCrowdCafeData(data):
		return HttpResponse(status=200, content = json.dumps({'score':1,'correct':True}))
	else:
		return HttpResponse(status=200, content = json.dumps({'score':-1,'correct':False}))

@csrf_exempt
def receiveJudgement(request):
	# to test - uncomment and open url in browser (comment lines below before 'for')
	#judgements  = [{'output_data': {u'_shapes': u'{"objects":[{"type":"image","originX":"left","originY":"top","left":0,"top":0,"width":1250,"height":704,"fill":"rgb(0,0,0)","stroke":null,"strokeWidth":1,"strokeDashArray":null,"strokeLineCap":"butt","strokeLineJoin":"miter","strokeMiterLimit":10,"scaleX":1,"scaleY":1,"angle":0,"flipX":false,"flipY":false,"opacity":1,"shadow":null,"visible":true,"clipTo":null,"backgroundColor":"","src":"http://www.ucarecdn.com/48aa063d-9589-4631-96cf-00c3effc2e5f/-/resize/600x/","filters":[],"crossOrigin":""},{"type":"polygon","originX":"left","originY":"top","left":282,"top":206,"width":1,"height":1,"fill":"green","stroke":"blue","strokeWidth":5,"strokeDashArray":null,"strokeLineCap":"butt","strokeLineJoin":"miter","strokeMiterLimit":10,"scaleX":1,"scaleY":1,"angle":0,"flipX":false,"flipY":false,"opacity":0.5,"shadow":null,"visible":true,"clipTo":null,"backgroundColor":"","points":[{"x":-0.5,"y":-0.5},{"x":16,"y":-73},{"x":34,"y":-109},{"x":116,"y":-140},{"x":147,"y":-135},{"x":729,"y":-55},{"x":673,"y":292},{"x":162,"y":436},{"x":2,"y":288}]}],"background":""}'}, 'score': 0.0, 'unit': 174, 'pk': 201, 'gold': False}]
	data = request.body
	judgements = json.loads(data)
	for item in judgements:
		# run this task in Celery as it takes time (27 seconds if we need to crop image, otherwise less)
		processCrowdCafeResult.delay(item)
	return HttpResponse(status=200)