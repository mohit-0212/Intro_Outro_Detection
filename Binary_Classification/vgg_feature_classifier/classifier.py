import pickle
import random
from sklearn.svm import LinearSVC
import shutil

positive_features = pickle.load(open("positive_features.pkl", "rb"))
negative_features = pickle.load(open("negative_features.pkl", "rb"))

x = []
y = []

for i, vec in enumerate(positive_features):
	x.append(vec)
	y.append(1)

for i, vec in enumerate(negative_features):
	x.append(vec)
	y.append(0)

combined = list(zip(x, y))
random.shuffle(combined)
x[:], y[:] = zip(*combined)


clf = LinearSVC()
clf.fit(x, y)

print clf.score(x, y)

x_test = []
y_test = []

# x_test.append(pickle.load(open("feat.pkl", "rb")))

# print clf.predict(x_test)


positive_features_test = pickle.load(open("positive_features_test.pkl", "rb"))
negative_features_test = pickle.load(open("negative_features_test.pkl", "rb"))


positive_images_test = pickle.load(open("positive_images_test.pkl", "rb"))
negative_images_test = pickle.load(open("negative_images_test.pkl", "rb"))
x_test_images = []

for i, vec in enumerate(positive_features_test):
	x_test_images.append(positive_images_test[i])
	x_test.append(vec)
	y_test.append(1)

for i, vec in enumerate(negative_features_test):
	x_test_images.append(negative_images_test[i])
	x_test.append(vec)
	y_test.append(0)

print clf.score(x_test, y_test)

y_pred = clf.predict(x_test)

d = {0:0, 1:0}

for i in range(len(y_test)):
	print y_test[i], y_pred[i]
	if y_test[i]==0:
		if y_pred[i]==1:
			shutil.copy2("./test_images/negatives/"+x_test_images[i], "./misclassified/pos/"+x_test_images[i])
			d[0]+=1
	elif y_test[i]==1:
		if y_pred[i]==0:
			shutil.copy2("./test_images/positives/"+x_test_images[i], "./misclassified/neg/"+x_test_images[i])
			d[1]+=1

print d


