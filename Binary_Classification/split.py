import os
import random
import shutil

train_dir = "./train/"

if not os.path.exists(train_dir):
	os.mkdir(train_dir)

test_dir = "./test/"

if not os.path.exists(test_dir):
	os.mkdir(test_dir)

data_dir = "./data/"
split_ratio = 0.75

videos = os.listdir(data_dir)
num_videos = len(videos)

random.shuffle(videos)
train = []
test = []

for i in range(num_videos):
	if i < int(split_ratio*num_videos):
		train.append(videos[i])
	else:
		test.append(videos[i])

for vid in train:
	shutil.copy2(data_dir+vid, train_dir+vid)


for vid in test:
	shutil.copy2(data_dir+vid, test_dir+vid)


