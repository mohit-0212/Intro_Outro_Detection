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

path = "the blacklist0001.jpg"
image = image_process(path)
vec = get_features(image)

pickle.dump(vec, open("feat.pkl", "wb"))