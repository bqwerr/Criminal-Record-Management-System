import logging
from .face_recognition import get_encoding, encode

def encode(key_points):
    encoded_string = ""
    for value in key_points[0]:
        svalue = str(value)
        if value < 0:
            svalue = svalue.replace('-', '1')  # Replace '-' with 1
        svalue = svalue.replace('.', '$')  # Replace . with $
        encoded_string = encoded_string + '@' + svalue
    return encoded_string

def get_key_points(image):
    """
    This method passes the base64 form image to get facialkey points.

    Returns
    -------
      list

    """
    result = None
    result = get_encoding(image)
    result = encode(result) # get key_points in string format
    return result

def decode(image):
    keypt = []
    keypt.append(image)
    encoded = []
    text = keypt[0].split('@')
    text = text[1:]
    for t in text:
        t = t.replace('$', '.')
        if t[0:1] == '1':
            t = '-' + t[1:]
        else:
            pass
        encoded.append(float(t))
    return encoded