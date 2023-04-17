# main file for running the camera
# id: camera-1
import requests
import datetime
import os
import shutil
import asyncio
import google_drive_handler

# import camera with model class
from camera import Camera
from utils import BACKEND_URL, PATH_TO_SAVE_IMAGES, DATE_FORMAT, TIME_FORMAT
from fetch_token import Token

async def main():
    while True:
        # camera.capture_image
        Camera.capture_image()
        
        now = datetime.datetime.now()
        time_string = now.strftime(TIME_FORMAT)
        # ex: camera_images/2023-03-05/00:07:40.png
        path = f'{PATH_TO_SAVE_IMAGES + "/" + now.strftime(DATE_FORMAT) + "/"+ time_string}.jpg'
        save_img = False
        
        if Camera.find_elephant_faster_rcnn_resnet152_model(): # return true if an elephant is found on the pic that has been scanned
            # save every image whether or not an elephant is found
            await Camera.save_image(path)
            save_img = True
            # # upload image and insert record to db in the background
            # task = asyncio.create_task(upload_img_and_insert_db(path))
            await upload_img_and_insert_db(path)
        
        if not save_img:
            await Camera.save_image(path)
        
        # delete old folder
        dirs = os.listdir(PATH_TO_SAVE_IMAGES)
        today = datetime.date.today()
        for directory in dirs:
            if not directory.startswith("."):
                date_object = datetime.datetime.strptime(directory, DATE_FORMAT).date()
                if today - date_object >= datetime.timedelta(days=2):
                    path = os.path.join(PATH_TO_SAVE_IMAGES, directory)
                    shutil.rmtree(path)
        await asyncio.sleep(10)

async def upload_img_and_insert_db(path):
    token = await Token.fetch_token()
    img_link = google_drive_handler.upload_picture(path)
    img_link = img_link.split("&export")[0]
    # sent req to backend
    req_obj = {"informant": "camera-1", "img_link": img_link}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url=f"{BACKEND_URL}/record", headers=headers, json=req_obj)
    print(response)
    
asyncio.run(main())