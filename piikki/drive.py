from __future__ import print_function
import httplib2
import os
from kivy.logger import Logger

import apiclient
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Kiltispiikki'
            
class DriveClient():

    
    def __init__(self):
        self.credentials = self.get_credentials()
        self.service = None
    
    def get_credentials(self):
        """Gets valid user credentials from storage.
    
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
    
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'drive-kiltispiikki.json')
    
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
	    try:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
	    except oauth2client.clientsecrets.InvalidClientSecretsError:
		Logger.info("Drive: invalid client secret, authentication failed")		    
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials    
        
    def connect(self):
        """Shows basic usage of the Google Drive API.
    
        Creates a Google Drive API service object and outputs the names and IDs
        for up to 10 files.
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)
        return service
    
         
    def upload_file(self, filename = None):
        if self.service == None:
            self.service = self.connect()
            if self.service == None:
                Logger.info('DriveClient: Connecting to drive failed')
                return
        #no filename given -> abort        
        if not filename: return False
            
        FILENAME = filename
        #filetype on drive, docs filetype required for export
        MIMETYPE = 'application/vnd.google-apps.document'
        #filename on this system and the name of the uploaded file on drive
        TITLE = FILENAME
        #general description
        DESCRIPTION = 'Csv list of account_name,customer_name,tab_value'
        #The Kiltispiikkivarmuuskopiot folder on hupi.mestarit drive
        PARENTFOLDER = '0BxdutqQIi9bzYWJsU0ExM2hUbXM'
        
        media_body = apiclient.http.MediaFileUpload(
                            FILENAME,
                            resumable=True
                        )
        # The body contains the metadata for the file. Name on drive
        body = {
          'description': DESCRIPTION,
          'name':TITLE,
          'parents':[PARENTFOLDER],
          'mimeType':MIMETYPE,
        }
        
        # Perform the request and print the result.
        self.service.files().create(body=body, media_body=media_body).execute()
        #return true if upload successful
        return True
        
    def download_latest_csv(self):
        if self.service == None:
            self.service = self.connect()
            if self.service == None:
                Logger.info('DriveClient: Connecting to drive failed')
                return
                
        results = self.service.files().list(
                    pageSize=10,fields="nextPageToken, files(id, name)",
                    q="'0BxdutqQIi9bzYWJsU0ExM2hUbXM' in parents",
                    orderBy="createdTime desc").execute()
        #import pprint
        #pprint.pprint(results)
        
        items = results.get('files', [])
        if not items:
            Logger.info('DriveClient: No files in the Kiltispiikki folder.')
            return
        else:
            download_id = items[0]['id']
            file1 = self.service.files().export(
                    fileId=download_id, mimeType='text/plain').execute()
            if file1:
                fn = items[0]['name']
                with open(fn, 'wb') as fh:
                    fh.write(file1)
                Logger.info('DriveClient: downloaded {}'.format(fn))                
            return items[0]['name']
                
   