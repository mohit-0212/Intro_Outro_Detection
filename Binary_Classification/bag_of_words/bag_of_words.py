import os
import cv2
import random
from sklearn.cluster import MiniBatchKMeans
from sklearn.svm import LinearSVC
import numpy as np

train_dir = "./train_images/"
test_dir = "./test_images/"
cluster_size = 32
size = (70, 40)
# size = (100, 60)

def load():
	x_train = []
	y_train = []

	x_test = []
	y_test = []

	for i in os.listdir(train_dir):
		for j in os.listdir(train_dir+i):
			img = cv2.imread(train_dir+i+"/"+j)
			# print train_dir+i+"/"+j
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			img = cv2.resize(img, size)
			# print img.shape
			x_train.append(img)
			if i=="positives":
				y_train.append(1)
			else:
				y_train.append(0)

	for i in os.listdir(test_dir):
		for j in os.listdir(test_dir+i):
			img = cv2.imread(test_dir+i+"/"+j)
			# print test_dir+i+"/"+j
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			img = cv2.resize(img, size)
			# print img.shape
			x_test.append(img)
			if i=="positives":
				y_test.append(1)
			else:
				y_test.append(0)
	print "loaded"
	return x_train, y_train, x_test, y_test


def cluster(x):
	sift = cv2.xfeatures2d.SIFT_create()
	x_desc = []
	for i in x:
		try:
			# gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
			kp, desc = sift.detectAndCompute(i, None)
			# print len(desc)
			# print len(desc[0])
			# for j in range(0, 5):
			for j in range(len(desc)):
				x_desc.append(np.array(desc[j]))
		except:
			pass
	print "SIFT created"
	kmeans = MiniBatchKMeans(n_clusters=cluster_size, random_state=0)
	# kmeans = KMeans(n_clusters=2, random_state=0, verbose=True, n_init = 1)
	kmeans.fit(np.array(x_desc))
	print "clustered"
	return kmeans
	# print kmeans.predict([x_desc[0]])


def train(kmeans, x_train, y_train, c):
	combined = list(zip(x_train, y_train))
	random.shuffle(combined)
	x_train[:], y_train[:] = zip(*combined)

	sift = cv2.xfeatures2d.SIFT_create()
	new_x_train = []
	for i in x_train:
		x_desc = [0.0 for j in range(cluster_size)]
		try:
			kp, desc = sift.detectAndCompute(i, None)
			pred = kmeans.predict(desc)
			for j in pred:
				x_desc[j]+=1
		except:
			pass
		new_x_train.append(x_desc)
	# print new_x_train
	clf = LinearSVC(C=c)
	clf.fit(new_x_train, y_train)
	print clf.score(new_x_train, y_train)
	print "training done"
	return clf

def test(clf, kmeans, x_test, y_test):
	sift = cv2.xfeatures2d.SIFT_create()
	new_x_test = []
	for i in x_test:
		x_desc = [0.0 for j in range(cluster_size)]
		try:
			kp, desc = sift.detectAndCompute(i, None)
			pred = kmeans.predict(desc)
			for j in pred:
				x_desc[j]+=1
		except:
			pass
		new_x_test.append(x_desc)
	# print new_x_test
	acc = clf.score(new_x_test, y_test)
	outs = clf.predict(new_x_test)
	print "testing"
	return acc, outs

def main():
	x_train, y_train, x_test, y_test = load()
	kmeans = cluster(x_train)
	clf = train(kmeans, x_train, y_train, 1)
	acc, outs = test(clf, kmeans, x_test, y_test)
	print acc

main()