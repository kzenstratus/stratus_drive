from django.shortcuts import render_to_response, render, RequestContext
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
# from django.core.files.base import ContentFile
from .forms import UploadFileForm
# from .forms import ModelFormWithFileField
# import os
# from settings import BASE_DIR
from django.http import HttpResponse
from stratus_drive.models import UserProfile, Drive
from django.core.exceptions import ObjectDoesNotExist
from strat import dropbox_registration_new, dropbox_login, \
									 google_registration, google_registration2, \
									google_login, google_upload, algorithm
# Create your views here
# home_page = None

def gateway(request):
	c = {}
	c.update(csrf(request))

	username = request.POST.get('username','')
	return render(request,'login_registration.html')
	

def home(request):
	form = UploadFileForm()
	# form = ModelFormWithFileField()
	args = {}
	args['form'] = form
	return render(request,'home.html', args, context_instance = RequestContext(request) )

def login(request):
	c = {}
	c.update(csrf(request))
	username = request.POST.get('username','')
	password = request.POST.get('password','')
	user = auth.authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			auth.login(request, user)
			return HttpResponseRedirect('/home')
	else:
		return render(request,'login.html')
	# user = auth.authenticate(username = username, password = password)
def logout(request):
	auth.logout(request)
	return render(request,'login_registration.html')

def registration(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('login.html')

	args = {}
# 	# args.update(csrf(request))
	args['form'] = UserCreationForm() #no information to put in it to start. 
# 	#Knows how to render it's fields but it doesn't know any data yet
	return render(request,'login_registration.html', args)

# def handle_upload_file(file):

def upload(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST)
		# form = ModelFormWithFileField(request.POST, request.FILES)
		# test = form.cleaned_data.get('file')
		# print test


		# form.save()
		print "I get here"
		up_dir =  request.POST.get('upload_dir')
		print up_dir
		# print form.upload_dir
		# for f in request.FILES.getlist('file'):
		# 	title = f.path
		# 	print "my title is" , title
		# 	f.save()
		person = request.user.id
		keys = UserProfile.objects.get(user_id =person)
		# print "my base dirrectory is ",BASE_DIR
		# temp_file_list = request.FILES.getlist('file')
		file_list = []

		# print request.POST['folder_name']
		# folder = request.path.replace("/", "_")
		# print request.path

		# for afile in temp_file_list:
		# 	instance = ModelFormWithFileField(file_field=afile)
		# 	instance.save()
		# 	print "hi " ,afile.name
		# 	file_list.append(afile.name)

		# try:
		# 	os.mkdir(os.path.join(BASE_PATH, folder))
		# except:
		# 	pass
		# full_filename = os.path.join(BASE_PATH, folder, file_list[0])
		# print "my full filename is " ,full_filename

		algorithm("Stratus_Folder",up_dir)


	return HttpResponseRedirect('/home')

# # d = [('tx1.txt',12345676), ('tx2.txt', 234232434), ('tx3.txt', 3434433)]
# folder_name = "file1"
# def upload(request):
# 	person = request.user.id

# 	form = Upload_Form(request.POST)
# 	folder_name = form['folder_name'].value() # keep this
# 	if form.is_valid():
# 		for field in form.fields:
# 			form.fields[field].required = False

# 	file_dic, bigfile = algorithm(folder_name)

# 	for key, value in file_dic.items():
# 		a = Drive(user_id = person, filename = key, service = value, parent = folder_name)
# 		a.save()
# 	args = {}
# 	# args.update(csrf(request))
# 	args['form'] = form;


# 	return render(request,'main.html',args)

# # def download(request):
# # 	person = request.user.id
# # 	# form = Download_Form(request.POST)
# # 	file_name = request.POST.get('file_name')
# # 	file_parent = request.POST.get('parent')
# # 	print file_parent
# # 	while file_parent:
# # 		file_name =  file_parent+"/"+file_name
# # 		file_parent = Drive.objects.get(parent = file_parent)

# # 	print file_name
# # 	# file_name = form['file_name'].value()
# # 	# print file_name
# # 	return render(request, 'main.html')

# def loggedin(request):

# 	drive_data = {}
# 	person = request.user.id
# 	try:
# 		keys = Tokens.objects.get(user = request.user)
# 		google_token = keys.google_token
# 		dropbox_token = keys.dropbox_token # test to see if both tokens are stored
# 		google_login()
# 		dropbox_login()
# 	except ObjectDoesNotExist:
# 		google_token = None
# 		dropbox_token = None
# # build user view

# 	drive_info = Drive.objects.all()
# 	drive_data["file_info"] = drive_info

# 	drive_data["username"] = request.user.username
# 		# count = count +1
# 	# drive_info = Drive.objects.all()
# 	return render(request,'main.html', drive_data)

# def invalid_login(request):
# 	return render_to_response('login.html')

# def logout(request):
# 	auth.logout(request)
# 	return render_to_response('logout.html')
# #Second time a user enters in our website
# def register_user(request): # if your user's information is correct
# 	if request.method == 'POST': #methods for forms (post or get)
# 		#first time around, no post
# 		form = UserCreationForm(request.POST) #pass through POST dictionary
# 		if form.is_valid():
# 			form.save()
# 			return HttpResponseRedirect('/accounts/register_success') 

# 	args = {}
# 	# args.update(csrf(request))
# 	args['form'] = UserCreationForm() #no information to put in it to start. 
# 	#Knows how to render it's fields but it doesn't know any data yet
# 	return render_to_response('login.html', args)

# def register_success(request):
# 	return render_to_response('main.html')