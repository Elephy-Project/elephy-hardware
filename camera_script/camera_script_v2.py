import cv2
import tensorflow as tf

import json

# load class
with open("faster_rcnn_resnet152_v1_640x640_1/mscoco_complete_label_map.json") as file:
    c = json.load(file)

classes = []
for i in c:
    classes.append(i["item"]["display_name"])


# load model
MODEL_PATH = "faster_rcnn_resnet152_v1_640x640_1"
model = tf.saved_model.load(MODEL_PATH)

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    input_frame = tf.expand_dims(rgb_frame, axis=0)
    input_frame = tf.image.resize(input_frame, (640, 640))
    input_frame = tf.cast(input_frame, dtype=tf.uint8)

    detections = model(input_frame)
    boxes = detections['detection_boxes'][0].numpy()
    class_ids = detections['detection_classes'][0].numpy().astype(int)
    scores = detections['detection_scores'][0].numpy()

    for i in range(len(boxes)):
        if scores[i] >= 0.7:
            ymin, xmin, ymax, xmax = boxes[i]
            # denormalized
            xmin = int(xmin * frame.shape[1])
            xmax = int(xmax * frame.shape[1])
            ymin = int(ymin * frame.shape[0])
            ymax = int(ymax * frame.shape[0])
            class_id = class_ids[i]
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(frame, classes[class_id], (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    cv2.waitKey(1)