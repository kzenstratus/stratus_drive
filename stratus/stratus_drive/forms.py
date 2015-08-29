from django import forms
from .models import UserProfile

class Drive_Token_Form(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('dropbox_token','google_token',)
		# def __init__(self, *args, **kwargs):
		# 	self.user = kwargs.pop('user', None)
		# 	super(Drive_Token_Form, self).__init__(*args, **kwargs)
			# return self.cleaned_data.get('user')
		# def clean_token(self):
		# 	username = self.cleaned_data.get('user')
		# 	if self.user and self.user.username == username:
		# 		return username
	 #        if UserProfile.objects.filter(user=username).count():
	 #            raise forms.ValidationError(u'That username already exists.')
	 #        return username



class Download_Form(forms.Form):
    file_name = forms.CharField(max_length = 300)