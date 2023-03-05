import cv2

# opencv DNN
# see more on yolo, mobilenet
network = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(network)

# more size = more precise predicting (bigger resolution) but slower processing
model.setInputParams(size=(320, 320), scale=1/255)

# load class lists
classes = []
with open("dnn_model/classes.txt", "r") as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        classes.append(class_name)


# initialize webcam, 0 = first webcam
cap = cv2.VideoCapture(0)

# resolution of the camera
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# create window
# "Frame" = window name
# click_button = function
# cv2.namedWindow("Frame")

# wait for camera to open
cv2.waitKey(1000)

while True:
    
    # get frames
    # ret: true if there is a frame
    ret, frame = cap.read()
    
    # object detection
    # frame = object on the specific frame
    # return 3 things: class of the object (id), 
    # score = confidence
    # bound boxes = box around the object, usually get the 2 coordinates of 
    # the top left corner, height, width
    (class_ids, scores, bboxes) = model.detect(frame)
    
    # may detect multiple objects
    # need to loop to get every object
    # zip() is a function to extract at the same time in the loop (multiple arrays)
    for class_id, score, bbox in zip(class_ids, scores, bboxes):
        # draw bounding box
        x, y, w, h = bbox
        
        # put text on the frame with str(class_id)
        # frame = frame to display
        # class_name = name of the class_id
        # (x, y - 5) = where to put the text
        # cv2.FONT_HERSHEY_PLAIN = font
        # 2 = size of the text
        # (200, 0, 50) = colour
        # 2 = thickness
        class_name = classes[class_id]
        cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        
        # draw rectangle on the frame
        # point 1 (x, y) = point on the top left
        # point 2 (x + w, y + h) = point on bottom right
        # colour of rectangle = (200, 0, 50)
        # thickness = 3
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        
    # print("class id ", class_ids)
    # print("score", scores)
    # print("bboxes", bboxes)
    
    
    cv2.imshow("Frame", frame)
    cv2.waitKey(1)


