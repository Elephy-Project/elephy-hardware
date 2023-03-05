# main file for running the camera
# id: camera-1
import requests
import time
import datetime
import os

# import camera with model class
from camera import Camera
from utils import BACKEND_URL, PATH_TO_SAVE_IMAGES, DATE_FORMAT



while True:
    # camera.capture_image
    Camera.capture_image()
    if Camera.find_elephant(): # return true if an elephant is found on the pic that has been scanned
        # sent req to backend
        req_obj = {"informant": "camera-1"}
        response = requests.post(url=f"{BACKEND_URL}/record", json=req_obj)
        print(response)
        
    Camera.save_image()
    
    # delete old folder
    dirs = os.listdir(PATH_TO_SAVE_IMAGES)
    today = datetime.date.today()
    for directory in dirs:
        date_object = datetime.datetime.strptime(directory, DATE_FORMAT).date()
        if today - date_object >= datetime.timedelta(days=2):
            path = os.path.join(PATH_TO_SAVE_IMAGES, directory)
            os.rmdir(path)
   
    time.sleep(10)