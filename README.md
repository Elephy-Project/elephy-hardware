# Elephy Camera

## Model set up
If Faster RCNN model is more prefered:
Download model from
```https://tfhub.dev/tensorflow/faster_rcnn/resnet152_v1_640x640/1```

Place `/variables` and `saved_model.pb` in `faster_rcnn_resnet152_v1_640x640_1` folder.
Ensure that in `main.py` `find_elephant_faster_rcnn_resnet152_model()` is used.

If YOLOV4 model is more preferred:
Change method `find_elephant_faster_rcnn_resnet152_model()` to `find_elephant_yolov4_model()`


## Google Drive Credentials
1. Enable Google Drive API
2. Create new project in google console and create OAuth 2.0 Client IDs.
3. Download client secret, edit file name to `credentials.json` and place the file at root.

## Set up .env
```
Variables in .env should include:
TOKEN_PATH
- Path to get jwt token to access to the resources from backend

USERNAME and PASSWORD
- Username and password of the user that has been registered in the database


SECRET_KEY and ALGORITHM
- Secret key and Algorithm to create jwt token in backend
```
## Run camera
### 1. Create environment
`python3 -m venv env`

### 2. Activate the environment
`. env/bin/activate`

### 3. Install requirements
`pip install -r requirements.txt`

### 4. Run camera
`python3 -m main.py`
