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