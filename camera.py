import cv2
import datetime
import os
from model import model, classes
from utils import PATH_TO_SAVE_IMAGES, DATE_FORMAT, TIME_FORMAT


class Camera:
    
    frame = None
    result = None

    def capture_image():
        cap = cv2.VideoCapture(0)
        # wait 1 second for camera to open
        cv2.waitKey(1000)
        Camera.result, Camera.frame = cap.read()
    
    def find_elephant() -> bool:
        """check if there is an elephant in the image

        Returns:
            bool: True if there is an elephant in the frame
        """
        # check if there is a frame
        if Camera.result:
            (class_ids, scores, bboxes) = model.detect(Camera.frame)
            for class_id, score, bbox in zip(class_ids, scores, bboxes):
                x, y, w, h = bbox
                class_name = classes[class_id]
                cv2.putText(Camera.frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                cv2.rectangle(Camera.frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                if class_name == "elephant" and score > 0.5:
                    return True
            return False
        
    def save_image():
        Camera.make_date_directory()
        now = datetime.datetime.now()
        time_string = now.strftime(TIME_FORMAT)
        # ex: camera_images/2023-03-05/00:07:40.png
        path = f'{PATH_TO_SAVE_IMAGES + "/" + now.strftime(DATE_FORMAT) + "/"+ time_string}.png'
        print(path)
        cv2.imwrite(path, Camera.frame)
        
    def make_date_directory():
        today = datetime.date.today()
        dirs = os.listdir(PATH_TO_SAVE_IMAGES)
        today_string = str(today)
        if today_string not in dirs:
            path = os.path.join(PATH_TO_SAVE_IMAGES, today_string)
            os.mkdir(path)
        
        
    
