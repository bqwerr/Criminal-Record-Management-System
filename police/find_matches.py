import base64
import time
import os
import pickle
import warnings
import io
import cv2
from PIL import Image
import numpy as np
from .face_recognition import face_encodings


model_name = 'classifier.pkl'

def get_base64_form(image):
    buff = io.BytesIO()
    image.save(buff, format="JPEG")
    img_str = base64.b64encode(buff.getvalue())
    return img_str

def decode_base64(img):
    img = img[1:]
    img = np.array(Image.open(io.BytesIO(base64.b64decode(img))))
    return img


def get_facial_points(img):
    return face_encodings(img)


def match(base64_image):
    if os.path.isfile(model_name):
        with open(model_name, 'rb') as f:
            (le, clf) = pickle.load(f)
    else:
        return "None"
    matched = []
    data = []
    image = decode_base64(str(base64_image))
    key_pts = get_facial_points(image)
    data.append([image, key_pts])
    for image, key_pts in data:
        closest_distances = clf.kneighbors(key_pts)
        is_recognized = [closest_distances[0][0][0] <= 0.5]
        # No clue why 'is True' is not working
        if is_recognized[0] == True:
            predictions = [(le.inverse_transform([pred]))
                           if rec else ("Unknown")
                           for pred, rec in zip(clf.predict(key_pts),
                                                is_recognized)]
            matched.append([predictions])
    return matched


