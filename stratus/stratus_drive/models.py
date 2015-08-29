from django.db import models
from django.utils.encoding import smart_unicode # when dealing with accents etc
from django.conf import settings
from django.contrib.auth.models import User

# from django.contrib.auth.models import User
# Create your models here.

# class UserExtra(models.Model):
# 	user = models.OneToOneField(settings.AUTH_USER_MODEL)
# 	def __unicode__(self):
# 		return str(self.first_time)

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	dropbox_token = models.CharField(max_length = 200, blank = True)
	google_token = models.CharField(max_length = 200, blank = True)

	# initial timestamp
	# timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
	# updated_time = models.DateTimeField(auto_now_add = False, auto_now = True)
	def __unicode__(self):
		return str(self.dropbox_token)
# class Crediential(models.Model):
# 	user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key = True)
# 	google_token = CredentialsField()


class Drive(models.Model):
	user = models.ForeignKey(User)
	filename = models.CharField(max_length = 100, default = "")
	memory = models.FloatField(default = 0)
	service = models.CharField(max_length = 50, default = "") #google/dropbox
	parent = models.CharField(max_length = 100, default = "") #references to a parent folder 
	def __unicode__(self):
		return str(self.service)

from django.contrib import admin
admin.site.register(Drive)