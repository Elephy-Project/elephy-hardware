import tensorflow as tf

import json

# load classes
with open("faster_rcnn_resnet152_v1_640x640_1/mscoco_complete_label_map.json") as file:
    c = json.load(file)

resnet152_classes = []
for i in c:
    resnet152_classes.append(i["item"]["display_name"])


# load model
MODEL_PATH = "faster_rcnn_resnet152_v1_640x640_1"
resnet152_model = tf.saved_model.load(MODEL_PATH)
