from django.db import models
from django.conf import settings
# 
# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')


# class Choice(models.Model):
#     question = models.ForeignKey(Question)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)


class UserExtra(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	twitter_handle = models.CharField(max_length=128)
# 	# user = models.OneToOneField(User)

class UploadFile(models.Model):
	folder_name = models.CharField(max_length = 300)
	upload_dir = models.CharField(max_length=300)
	# file = models.FileField(label='Select a file')

# 	def __unicode__(self):
# 		return '{} extra'.format(self.user)



# from django.contrib import admin
# admin.site.register(UserExtra)

# User.UserExtra = property(lambda u: Vendor.objects.get_or_create(user=u)[0])