from oauth2client.file import Storage
import httplib2
import pprint
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from apiclient import errors #for downloading
import dropbox
import os


DROPBOX_APP_KEY = 'ezxw256lfwnlriz'
DROPBOX_APP_SECRET = 'qapvcsm65nfufhm'
GOOGLE_CLIENT_ID = '648983292705-v3jnqrj51lao8f1h98tpubqhe6jj1r7k.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '8T7PCnHyB9CkZckwjrY0WIvK'
GOOGLE_OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
GOOGLE_REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
google_flow = OAuth2WebServerFlow(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_OAUTH_SCOPE,
                                redirect_uri=GOOGLE_REDIRECT_URI)
dropbox_flow = dropbox.client.DropboxOAuth2FlowNoRedirect(DROPBOX_APP_KEY, DROPBOX_APP_SECRET)

################################################################################################

# folder = 'uploads/'
dict_ = {}

def algorithm(foldername, upload_dir):

  print 'currently running the algorithm'
  ###########################################
  #obtain connection to accounts 
  client = dropbox_login()
  drive_service = google_login()
  about = drive_service.about().get().execute()
  ###########################################
  #####################################################
  # compute space left on user's accounts in bytes

  total_space_dropbox = float(client.account_info()['quota_info']['quota'])
  used_space_dropbox = float((client.account_info()['quota_info']['normal']) + float(client.account_info()['quota_info']['shared']))
  space_left_dropbox = total_space_dropbox - used_space_dropbox
  space_left_dropbox_percent = (space_left_dropbox / total_space_dropbox) * 100 

  used_space_MB_ = used_space_dropbox / 1000000
  space_left_MB = space_left_dropbox / 1000000

  total_space_google = float(about['quotaBytesTotal'])
  used_space_google = float(about['quotaBytesUsed']) + float(about['quotaBytesUsedInTrash'])
  space_left_google = (total_space_google) - (used_space_google)

  space_left_google_percent = (space_left_google / total_space_google) * 100

  ########################################################
  # dictionary returned to website to display where the files have been placed 

  dict_added = {}
  big_files = {}

  #######################################################
  #find total size of all files about to be uploaded
  list_of_files = os.listdir(upload_dir)
  # list_of_files = upload_dir
  package_size = files_size(list_of_files, upload_dir)
  print list_of_files
  print package_size
  print " % space left on Google Drive: " + str(space_left_google_percent) + "%"
  print " Percentage of space left on Dropbox: " + str(space_left_dropbox_percent) + "%"
  stratus_id = get_stratus_folder_id()
  ######################################################

  #if all of these files fit into dropbox 
  if ((space_left_dropbox - package_size) >= 0):
    # and dropbox has more open space than google 
    if ((space_left_dropbox_percent - space_left_google_percent) >= 0):  
      print "Dropbox has more open space than Google Drive and files fit into Dropbox"
      return allocate_files(upload_dir, list_of_files,client,foldername,'dropbox', dict_added, big_files, stratus_id)
    # dropbox has less space than google and it fits into google
    elif ((space_left_google - package_size) >= 0):
      print "Dropbox has less space and files fit into Google"
      return allocate_files(upload_dir,list_of_files, drive_service, foldername, 'google', dict_added, big_files, stratus_id)
    # dropbox has less space but files do not fit into google
    else :
      print "Dropbox has less space but files do not fit into Google"
      return allocate_files(upload_dir,list_of_files, client, foldername, 'dropbox', dict_added, big_files, stratus_id)
  #Can't fit into dropbox but can fit into google
  elif ((space_left_google - package_size) >= 0):
    print ''
    return allocate_files(upload_dir,list_of_files, drive_service, foldername, 'google', dict_added, big_files, stratus_id)
  #Can't fit into any storage as a group
  else: 
    print "Can't be stored as a group" 
    dict_added, big_files = allocate_files_individually(list_of_files, client, drive_service, foldername, dict_added,  big_files, stratus_id)
  return dict_added, big_files



def files_size(list_of_files,upload_dir):
  sum = 0
  print upload_dir, "THIS IS IT"
  for file_ in list_of_files:
    print file_
    sum = sum + os.path.getsize(upload_dir + "/"+file_)
  return sum  

#allocates files in a group
def allocate_files(upload_dir,list_of_files, app_info, foldername, app, dict_added, big_files, stratus_id):
  print '6'
  
  if app == 'dropbox':
    for file_ in list_of_files:
      dropbox_upload(upload_dir,file_, app_info, foldername)
      dict_added[file_] = 'dropbox'
  else :
    for file_ in list_of_files:
      #folder_id = google_create_sub_folder(app_info,foldername, stratus_id )
      if file_[len(file_)-1] == '~':
        continue
      print file_

      google_upload(upload_dir,file_, app_info, foldername, stratus_id)
      dict_added[file_] = 'google'
      print dict_added
  return dict_added, big_files

#if files need to be seperated and put in seperately 
def allocate_files_individually(upload_dir,list_of_files,client, drive_service, foldername, dict_added, big_files, stratus_id):
  #files that are too big to fit and are not uploaded 

  print '7'
  for file_ in list_of_files:
    file_size = os.path.getsize(upload_dir + "/" + file_)
    file_name = file_
    #if file fits into dropbox
    if ((space_left_dropbox - file_size)  >= 0):
      dropbox_upload(folder, file_ , client, foldername)
      dict_added[file_name] = 'dropbox'
    #doesn't fit into dropbox but fits into google
    elif ((space_left_google - tuple_size) >= 0):
      print dict_ 
      print dict_added
      #folder_id = google_create_sub_folder(drive_service,foldername, stratus_id)
      google_upload(upload_dir ,file_name, app_info, foldername, stratus_id)
      dict_added[file_name] = 'google'
    #does not fit anywhere
    else :
      big_files[file_name] = file_size
      continue
  return dict_added, big_files
    




##################################################################################################

    
def dropbox_registration_old(key):
  key = key.strip()
  access_token, user_id = dropbox_flow.finish(key)
  f = open('access_token.txt','w')
  f.write(access_token)
  f.close()

def dropbox_registration_new(input):
  authorize_url = dropbox_flow.start()
  print 'Go to: ' + authorize_url
  print 'Copy the authorization code'
  # key = raw_input("Enter the authorization code here: ").strip()
  key = input.strip()
  access_token, user_id = dropbox_flow.finish(key)
  f = open('access_token.txt', 'w')
  f.write(access_token)
  f.close()

def dropbox_login():
  g = open('access_token.txt','r')
  access_token = g.readlines()[0]
  g.close()
  client = dropbox.client.DropboxClient(access_token)
  print 'Dropbox linked account: ', client.account_info()
  return client

def dropbox_upload(filename, client, foldername = '' ):
  f = open(filename, 'rb')
  response = client.put_file('/Stratus/'+ foldername +'/' + filename, f)
  print 'uploaded: ', response

  folder_metadata = client.metadata('/')
  print 'metadata: ', folder_metadata


def dropbox_download(filename, client, foldername):   
  f, metadata = client.get_file_and_metadata('Stratus/' + foldername + '/' + filename)
  out = open(filename, 'wb')
  out.write(f.read())
  out.close()
  return metadata


########################GOOGLE DRIVE CODE##################################

def google_registration(input):
  #This function is used to register user's google accounts with Stratus
  #We save their credentials 
  authorize_url = google_flow.step1_get_authorize_url()
  print 'Go to the following link in your browser: ' + authorize_url
  key = input.strip()
  google_registration2(key)

def google_registration2(key):
  credentials = google_flow.step2_exchange(key) #token was previously "credentials"
  storage = Storage('credentials.txt')
  storage.put(credentials)
  #stratus_id = create_folder(drive_service, "Stratus")
  return storage 

def google_login():
  storage = Storage('credentials.txt')
  #This function is used to make a connection with Google API for those that
  #have already registered their google acount with Stratus
  token = storage.get()
  # Create an httplib2.Http object and authorize it with our credentials
  http = httplib2.Http()
  http = token.authorize(http)

  drive_service = build('drive', 'v2', http=http)
  
  if 'stratus_folder_id.txt' not in os.listdir('.'):
    stratus_id = create_folder(drive_service, "Stratus")
    f = open('stratus_folder_id.txt','w')
    f.write(stratus_id)
    f.close() 
    
  return drive_service
  

def get_stratus_folder_id():
  
  g = open('stratus_folder_id.txt', 'r')
  stratus_id = g.readlines()[0]
  g.close()

  return stratus_id

def create_folder(drive_service, folder_name):
  #Automatically make Stratus folder upon registration
  #POST https://www.googleapis.com/drive/v2/files
  #Authorization: Bearer {credentials}
  #Content-Type: application/json

  body = {
    'title': folder_name,
    "mimeType": "application/vnd.google-apps.folder"
  }

  file_ = drive_service.files().insert(body=body).execute()
  #pprint.pprint(file)
  

  return file_['id']

def google_create_sub_folder(drive_service, folder_name, parent_id):
  
  body = {
    'title': folder_name,
    "mimeType": "application/vnd.google-apps.folder",
    "parents": [{'id': parent_id}]
  }

  file_ = drive_service.files().insert(body=body).execute()
  
  dict_[file_['title']] = file_['id']

  return file_['id']  


def check_folders(folder_name):
  if folder_name in (dict_.keys()):
    return str(dict_[folder_name])
  else:
    return 'none'

def find_parent_id(drive_service, folder_name, stratus_id):
  #print stratus_id
  parent_id = check_folders(folder_name)
  if parent_id == 'none':
    new_id = google_create_sub_folder(drive_service, folder_name, stratus_id)
    return new_id
  else:
    return parent_id


def google_upload(upload_dir,filename, drive_service, foldername, stratus_id):
  parent_id = find_parent_id(drive_service, foldername, stratus_id)

  # Insert a file
  # media_body = MediaFileUpload('uploads/' + filename, resumable=True,)
  media_body = MediaFileUpload(upload_dir + "/"+filename, resumable=True,)
  
  body = {
    'title':filename,
    'description': 'Testing',
    'parents': [{'id': parent_id}]
  }

  file_ = drive_service.files().insert(body=body, media_body=media_body).execute()
  #pprint.pprint(file)

  print "Upload Succesful"

  return 


def google_download_file(drive_file, drive_service,):
  """Download a file's content.

  Args:
    drive_service: Drive API service instance.
    drive_file: Drive File instance.

  Returns:
    File's content if successful, None otherwise.
  """
  download_url = drive_file.get('downloadUrl')
  if download_url:
    resp, content = drive_service._http.request(download_url)
    if resp.status == 200:
      print 'Status: %s' % resp
      return content
    else:
      print 'An error occurred: %s' % resp
      return None
  else:
    # The file doesn't have any content stored on Drive.
    return None

def google_web_get(self):
  """Called when HTTP GET requests are received by the web application.

  Use the query parameter file_id to fetch the required file's metadata then
  content and return it as a JSON object.

  Since DrEdit deals with text files, it is safe to dump the content directly
  into JSON, but this is not the case with binary files, where something like
  Base64 encoding is more appropriate.
  """
  # Create a Drive service
  service = self.CreateDrive()
  if service is None:
    return
  try:
    # Requests are expected to pass the file_id query parameter.
    file_id = self.request.get('file_id')
    if file_id:
      # Fetch the file metadata by making the service.files().get method of
      # the Drive API.
      f = service.files().get(fileId=file_id).execute()
      downloadUrl = f.get('downloadUrl')
      # If a download URL is provided in the file metadata, use it to make an
      # authorized request to fetch the file ontent. Set this content in the
      # data to return as the 'content' field. If there is no downloadUrl,
      # just set empty content.
      if downloadUrl:
        resp, f['content'] = service._http.request(downloadUrl)
      else:
        f['content'] = ''
    else:
      f = None
    # Generate a JSON response with the file data and return to the client.
    self.RespondJSON(f)
  except AccessTokenRefreshError:
    # Catch AccessTokenRefreshError which occurs when the API client library
    # fails to refresh a token. This occurs, for example, when a refresh token
    # is revoked. When this happens the user is redirected to the
    # Authorization URL.
    self.RedirectAuth()

def google_web_post(self):
  """Called when HTTP POST requests are received by the web application.

  The POST body is JSON which is deserialized and used as values to create a
  new file in Drive. The authorization access token for this action is
  retreived from the data store.
  """
  # Create a Drive service
  service = self.CreateDrive()
  if service is None:
    return

  # Load the data that has been posted as JSON
  data = self.RequestJSON()

  # Create a new file data structure.
  resource = {
    'title': data['title'],
    'description': data['description'],
    'mimeType': data['mimeType'],
  }
  try:
    # Make an insert request to create a new file. A MediaInMemoryUpload
    # instance is used to upload the file body.
    resource = service.files().insert(
        body=resource,
        media_body=MediaInMemoryUpload(
            data.get('content', ''),
            data['mimeType'],
            resumable=True)
    ).execute()
    # Respond with the new file id as JSON.
    self.RespondJSON(resource['id'])
  except AccessTokenRefreshError:
    # In cases where the access token has expired and cannot be refreshed
    # (e.g. manual token revoking) redirect the user to the authorization page
    # to authorize.
    self.RedirectAuth()


######################################################################################


#def introduction():
  print "Welcome to Stratus!"
  first_time = raw_input('Are you a first time user? (yes/no) ').strip()
  if first_time == "yes":
    print "\nThank you for choosing Stratus \n"
    return first_time
  elif first_time == "no":
    print "\nWelcome back user!\n"
    return first_time
  else:
    print "Invalid Response, try again"
    introduction() 

#if __name__ == "__main__":
  #first_time = introduction()


def dropbox_auth_start(web_app_session, request):
    authorize_url = get_dropbox_auth_flow(web_app_session).start()
    redirect_to(authorize_url)

def dropbox_auth_finish(web_app_session, request):
    try:
        access_token, user_id, url_state = \
                get_dropbox_auth_flow(web_app_session).finish(request.query_params)
    except DropboxOAuth2Flow.BadRequestException, e:
        http_status(400)
    except DropboxOAuth2Flow.BadStateException, e:
        # Start the auth flow again.
        redirect_to("/dropbox-auth-start")
    except DropboxOAuth2Flow.CsrfException, e:
        http_status(403)
    except DropboxOAuth2Flow.NotApprovedException, e:
        flash('Not approved?  Why not?')
        return redirect_to("/home")
    except DropboxOAuth2Flow.ProviderException, e:
        logger.log("Auth error: %s" % (e,))
        http_status(403)