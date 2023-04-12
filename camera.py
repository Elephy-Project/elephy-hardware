import cv2
from model import model, classes
from utils import make_date_directory


class Camera:
    
    frame = None
    result = None

    def capture_image():
        cap = cv2.VideoCapture(0)
        # wait 1 second for camera to open
        cv2.waitKey(1000)
        Camera.result, Camera.frame = cap.read()
    
    def find_elephant():
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
        
    def save_image(path):
        make_date_directory()
        cv2.imwrite(path, Camera.frame)

