from django.utils.translation import ugettext_lazy as _
from django import forms

# class UploadFileForm(forms.Form):
# 	folder_name = forms.CharField(max_length = 300)
# 	# title = forms.CharField(max_length=50)
# 	file = forms.FileField(label='Select a file')
class UploadFileForm(forms.Form):


	folder_name = forms.CharField(max_length = 300)
	upload_dir = forms.CharField(max_length=300)
	# file = forms.FileField(label='Select a file')

# class ModelFormWithFileField(forms.Form):
