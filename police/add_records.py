import io
import base64
import json
import numpy as np
import PIL
from .face_encoding import get_key_points

'''
img - Image
base64_image / encoded_image - bytes
result - boolean

'''

def get_base64_form(image):
    buff = io.BytesIO()
    image.save(buff, format="JPEG")
    img_str = base64.b64encode(buff.getvalue())
    return img_str

def generate(base64_image):
    # generate key points
    key_points = get_key_points(base64_image)
    print("key_points in str format", key_points)
    return key_points