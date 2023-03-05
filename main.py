# main file for running the camera
# id: camera-1
import requests
import time

# import camera with model class
from camera import Camera

# url to backend
BACKEND_URL = 'https://elephy-backend.vercel.app'



while True:
    # camera.capture_image
    Camera.capture_image()
    if Camera.find_elephant(): # return true if an elephant is found on the pic that has been scanned
        # sent req to backend
        req_obj = {"informant": "camera-1"}
        response = requests.post(url=f"{BACKEND_URL}/record", json=req_obj)
        print(response)
        
    Camera.save_image()
    time.sleep(10)


    # TODO: delete pics that have been taken 1 day ago.
    # approx. 1440 pics if a pic is captured every 10 secs.
