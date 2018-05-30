import os
import subprocess
import json
import random

with open("annotation.json","r") as f:
  data = f.read()


annotation = json.loads(data)


def frame_extract(dire, pos, neg):
	vids = os.listdir(dire)
	positives = pos
	negatives = neg
	# random.shuffle(vids)
	for i, show in enumerate(vids):
		print i, show
		print
		name = show.split(".")[0]
		pos_beg = annotation[name]["intro_start"]
		pos_end = annotation[name]["intro_end"]
		neg_beg = pos_beg.split(":")[0] + ":" + str(int(pos_beg.split(":")[1])+2) + ":" + "00"
		neg_end = neg_beg.split(":")[0] + ":" + str(int(neg_beg.split(":")[1])+1) + ":" +  neg_beg.split(":")[2]
		# print pos_beg, pos_end
		# print neg_beg, neg_end
		# print show
		# print train_dir+show
		pos_cmd = "ffmpeg -i " + "'" + dire + show + "'" + " -ss " + pos_beg + " -to " + pos_end + " -vf fps=1 " + "'" + positives + name + "'" + "%04d.jpg -hide_banner"	
		subprocess.call(pos_cmd, shell = True)
		neg_cmd = "ffmpeg -i " + "'" + dire + show + "'" + " -ss " + neg_beg + " -to " + neg_end + " -vf fps=1 " + "'" + negatives + name + "'" + "%04d.jpg -hide_banner"	
		subprocess.call(neg_cmd, shell = True)
		print

# dire = "./train/"
# pos = "./train_images/positives/"
# neg = "./train_images/negatives/"

dire = "./test/"
pos = "./test_images/positives/"
neg = "./test_images/negatives/"


frame_extract(dire, pos, neg)
