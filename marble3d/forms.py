from django import forms
from datetime import date, timedelta
from models import Block, Image
from django.contrib.auth.models import User

from django.conf import settings

from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, Layout

from django.forms.forms import Form


class BlockForm(ModelForm):
	user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)

	class Meta:
		model = Block

	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))
		self.helper.form_class = 'form-vertical'
		super(BlockForm, self).__init__(*args, **kwargs)

class ImageForm(ModelForm):
	block = forms.ModelChoiceField(queryset=Block.objects.all(), widget=forms.HiddenInput)
	class Meta:
		model = Image
		exclude = ('date_created',)
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))
		self.helper.form_class = 'form-vertical'
		super(ImageForm, self).__init__(*args, **kwargs)