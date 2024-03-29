import os
import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from utils import TIME_FORMAT


creds = None
SCOPES = ['https://www.googleapis.com/auth/drive']
PARENT_FOLDER_ID='1tSmexPSuwZb9AO2nFZdR-JFJ_6o6zdZ4'

def create_file_name():
    now = datetime.datetime.now()
    time_string = now.strftime(TIME_FORMAT)
    # ex 00:07:40.jpg
    file_name = time_string + '.jpg'
    return file_name

def push_to_drive(service, parent_folder_id, file_name, path_to_file):
    file_metadata = {'name': file_name, 'parents': [parent_folder_id]}
    media = MediaFileUpload(path_to_file, mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')
    print('File ID: %s' % file_id)
    return True, file_id

def get_link_from_file_id(service, file_id):
    file = service.files().get(fileId=file_id, fields='webContentLink').execute()
    link = file.get('webContentLink')
    return link

# get access
def get_access_token():
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# service object for google drive api
def upload_picture(path_to_file):
    try:
        creds = get_access_token()
        service = build('drive', 'v3', credentials=creds)
        
        folders = service.files().list(q=f"'{PARENT_FOLDER_ID}' in parents and trashed = false",
                               fields="nextPageToken, files(id, name)").execute()
        items = folders.get('files', [])
        folder_exist = False
        today_string = str(datetime.date.today())
        file_name = create_file_name()
        for item in items:
            if item['name'] == today_string:
                file, file_id = push_to_drive(service, item['id'], file_name, path_to_file)
                img_link = get_link_from_file_id(service, file_id)
                folder_exist = True
                return img_link
        
        if not folder_exist:
            folder_metadata = {'name': today_string, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [PARENT_FOLDER_ID]}
            folder = service.files().create(body=folder_metadata, fields='id').execute()
            print('Folder ID: %s' % folder.get('id'))
            file, file_id = push_to_drive(service, folder.get('id'), file_name, path_to_file)
            img_link = get_link_from_file_id(service, file_id)
            return img_link
        
        if not file:
            raise Exception

    except HttpError as error:
        print(f'An error occurred: {error}')

    except Exception as e:
        print("Error occur: ", e)
