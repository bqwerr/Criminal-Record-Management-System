import pickle
import os

from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from .models import *
from .face_encoding import decode
import numpy as np


model_name = "classifier.pkl"

def fetch_data():
    labels = []
    key_points = []
    for record in CrimeRecords.objects.all().iterator():
        unique_label, encoded_image = record.key, record.key_points
        
        labels.append(unique_label)
        decoded_image = decode(encoded_image)
       
        key_points.append(decoded_image)
   
    return labels, np.array(key_points)

def start_train():
    if os.path.isfile('classifier.pkl'):
        os.remove('classifier.pkl')
    labels, key_pts = fetch_data()  
    le = LabelEncoder()
    encoded_labels = le.fit_transform(labels)
    classifier = KNeighborsClassifier(n_neighbors=len(labels),
                                        algorithm='ball_tree',
                                        weights='distance')
    classifier.fit(key_pts, encoded_labels)
    with open(model_name, 'wb') as file:
        pickle.dump((le, classifier), file)
    return True
    # except Exception as e:
    #     print(str(e))
    #     return False

