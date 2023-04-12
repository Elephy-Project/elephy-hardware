import datetime
import os


PATH_TO_SAVE_IMAGES="camera_images"
DATE_FORMAT="%Y-%m-%d"
DATETIME_FORMAT="%d-%m-%Y_%H:%M:%S"
TIME_FORMAT="%H:%M:%S"

BACKEND_URL='https://elephy-backend.vercel.app'


def make_date_directory():
    today = datetime.date.today()
    dirs = os.listdir(PATH_TO_SAVE_IMAGES)
    today_string = str(today)
    if today_string not in dirs:
        path = os.path.join(PATH_TO_SAVE_IMAGES, today_string)
        os.mkdir(path)