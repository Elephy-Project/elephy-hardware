import cv2
import tensorflow as tf

from yolov4_model import yolov4_model, yolov4_classes
from faster_rcnn_resnet152 import resnet152_model, resnet152_classes
from utils import make_date_directory
from PIL import Image


class Camera:
    
    frame = None
    result = None

    def capture_image():
        cap = cv2.VideoCapture(0)
        # wait 1 second for camera to open
        cv2.waitKey(1000)
        Camera.result, Camera.frame = cap.read()
    
    def find_elephant_yolov4_model():
        """check if there is an elephant in the image

        Returns:
            bool: True if there is an elephant in the frame
        """
        # check if there is a frame
        if Camera.result:
            (class_ids, scores, bboxes) = yolov4_model.detect(Camera.frame)
            for class_id, score, bbox in zip(class_ids, scores, bboxes):
                x, y, w, h = bbox
                class_name = yolov4_classes[class_id]
                cv2.putText(Camera.frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                cv2.rectangle(Camera.frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                if class_name == "elephant" and score > 0.5:
                    return True
            return False
    
    def find_elephant_faster_rcnn_resnet152_model():
        """check if there is an elephant in the image

        Returns:
            bool: True if there is an elephant in the frame
        """
        # check if there is a frame
        if Camera.result:
            rgb_frame = cv2.cvtColor(Camera.frame, cv2.COLOR_BGR2RGB)

            input_frame = tf.expand_dims(rgb_frame, axis=0)
            input_frame = tf.image.resize(input_frame, (640, 640))
            input_frame = tf.cast(input_frame, dtype=tf.uint8)

            detections = resnet152_model(input_frame)
            boxes = detections['detection_boxes'][0].numpy()
            class_ids = detections['detection_classes'][0].numpy().astype(int)
            scores = detections['detection_scores'][0].numpy()
            
            for i in range(len(boxes)):
                score = scores[i]
                class_name = resnet152_classes[class_ids[i]]
                if score >= 0.6:
                    # tl = top left, br = bottom right
                    tl_y, tl_x, br_y, br_x = boxes[i]

                    # denormalized
                    tl_x = int(tl_x * Camera.frame.shape[1])
                    br_x = int(br_x * Camera.frame.shape[1])
                    tl_y = int(tl_y * Camera.frame.shape[0])
                    br_y = int(br_y * Camera.frame.shape[0])
                    
                    cv2.rectangle(Camera.frame, (tl_x, tl_y), (br_x, br_y), (0, 255, 0), 2)
                    cv2.putText(Camera.frame, class_name, (tl_x, tl_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                if class_name == "elephant" and score >= 0.7:
                    return True
            return False
    
    def image_compress(path):
        # image compression
        # reduce the quality 50% and change to jpeg
        image = Image.open(path)
        compression_level = 50
        print(path)
        image.save(path, quality=compression_level)
    
    async def save_image(path):
        make_date_directory()
        cv2.imwrite(path, Camera.frame)
        Camera.image_compress(path)
