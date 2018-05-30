from time import time
from keras.models import Sequential, Model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
# from keras.applications.resnet50 import ResNet50
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import VGG16
import math
import numpy as np
import pickle
import os

model = VGG16()
featuremodel = Model(inputs=model.layers[0].input, outputs=model.layers[-2].output)

def image_process(path):
	image = load_img(path, target_size=(224, 224))
	image = img_to_array(image)
	image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
	image = preprocess_input(image)
	return image

def get_features(img):
	fvec = featuremodel.predict(img)[0,:]
	normfvec = math.sqrt(fvec.dot(fvec))
	vec = fvec/normfvec	
	return vec

print "Positives started"

positives = "./train_images/positives/"
pos_frames = os.listdir(positives)
print len(pos_frames)
pos_features = []

for frame in pos_frames:
	path = positives + frame
	image = image_process(path)
	vec = get_features(image)
	pos_features.append(vec) 

print "Positives Done"

with open("positive_features","wb") as f:
  pickle.dump(pos_features, f)

print "Positives stored"

print "Negatives started"

negatives = "./train_images/negatives/"
neg_frames = os.listdir(negatives)
neg_features = []

for frame in neg_frames:
	path = negatives + frame
	image = image_process(path)
	vec = get_features(image)
	neg_features.append(vec) 

print "Negatives done"

with open("negative_features","wb") as f:
  pickle.dump(neg_features, f)

print "Negatives stored"