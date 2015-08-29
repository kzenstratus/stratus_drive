from django.shortcuts import render, render_to_response, RequestContext
from .forms import Drive_Token_Form
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from stratus_drive.models import UserProfile, Drive
from django.core.exceptions import ObjectDoesNotExist
from strat import dropbox_registration_new, dropbox_login, \
									 google_registration, google_registration2, \
									google_login, google_upload, algorithm
# from .models import UserProfile

def register_drives(request):
	try:
		profile = request.user.userprofile
	except UserProfile.DoesNotExist:
		profile = UserProfile(user=request.user)


	if request.method == 'POST':
		person = request.user.id #request user's id, get token, enter into registration
		form = Drive_Token_Form(request.POST, instance = profile)
		print 'HERE IS MY USERNAME', person

		try:
			keys = UserProfile.objects.get(user_id =person)
			google_token = keys.google_token
			dropbox_token = keys.dropbox_token
			print "GOOGLE REGISTRATION IS NONE", keys
			print 'My google token is ', google_token
		except ObjectDoesNotExist:
			google_token = None
			dropbox_token = None
			print 'I set my tokens = None'
		# print keys.dropbox_token
		# print type(keys.google_token)
		if(google_token == ""):
			print "SUCCESS FOUND IT "
		drive_dic = {"google_token": google_token,"dropbox_token": dropbox_token}
		new_update = False
		old_user = False
		# Tells us if there are still empty fields that need to be filled
		for drive in drive_dic:
			if drive_dic[drive] == None or drive_dic[drive] == "":
				print drive
				new_update = True
				temp_goog = form["google_token"].value()
				temp_drop = form["dropbox_token"].value()
				if drive == "google_token" and temp_goog != "":
					print "my drive is google_token and I havfe an input which is "
					google_token = temp_goog
					google_registration(google_token)
				elif drive == "dropbox_token" and form.fields['dropbox_token'] != "":
					dropbox_token = temp_drop
					dropbox_registration_new(dropbox_token)
			else:
				old_user = True
		if new_update: #checks to see if they already have a google token->starts flow

			print "REGISTERING GOOGLE "
			# print keys.dropbox_token
			if form.is_valid():
				form.save()
			# print "google is ", form.google_token
			print "dropbox is ", form.fields['dropbox_token'], type(form.fields['dropbox_token'])
			return HttpResponseRedirect('home')
	else:
		form = Drive_Token_Form(instance = profile)
	args = {}
	# args.update(csrf(request))
	args['form'] = form
	return render(request,'register_drives.html',args, context_instance = RequestContext(request))

# {'username':request.user.username},
def register_drives_success(request):
	return render_to_response('home')