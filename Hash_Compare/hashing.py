# import cv2
import imagehash
from PIL import Image
from time import time
import subprocess
import os


# def get_hashList(path):
# 	hashList = []
# 	vid_frame = cv2.VideoCapture(path)
# 	length = vid_frame.get(cv2.CAP_PROP_FRAME_COUNT)
# 	fps = vid_frame.get(cv2.CAP_PROP_FPS)
# 	num_frames = int(fps*300)
# 	for i in range(0, num_frames):
# 		print (i+1,"/",num_frames)
# 		success, image = vid_frame.read()
# 		if i%1 == 0:
# 			if success:
# 				cv_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# 				pil_img = Image.fromarray(cv_img)
# 				hashList.append(imagehash.phash(pil_img))
# 	return hashList

def get_hash(path):
	return imagehash.phash(Image.open(path))

def common_elements(list1, list2):
	common = []
	for i, element in enumerate(list1):
		# if element in list2:
			# common.append(element)
		try:
			ind = list2.index(element)
			common.append((ind, i))
		except:
			pass
	return common

def get_timings(out):
	to_find = "pts_time:"
	length = len(to_find)
	loc = -1
	times = []
	while True:
		loc = out.find(to_find, loc + 1)
		if loc == -1:
			break
		time = ""
		current = loc + length
		while out[current]!=" ":
			time+=out[current]
			current+=1
		times.append(time)
	del times[-1]
	return times

def get_scene_images(path):
	threshold = 0.35
	end_time = 360 #in seconds

	name = path.split("/")[-1].split(".")[0]
	# print (name)

	if not os.path.exists("./" + name +"/"):
		os.mkdir(name)

	input_file = path

	scenes = "ffmpeg -i '" + input_file + "' -ss 0 -to 360" + ' -vf  "select=' + "'gt(scene," + str(threshold) + ")'," + 'showinfo" -vsync vfr "./' + name + '/' + name + '"%04d.jpg>scenes 2>&1'
	# print (scenes)
	subprocess.call(scenes, shell = True)

	file = open("scenes", "r")
	out = file.read()
	file.close()
	times = get_timings(out)

	# print len(times)
	# print times
	# times = [float(i) for i in times]

	os.remove("./scenes")
	return times


def get_hash_from_dir(path):
	images = os.listdir(path)
	images.sort()
	hashlist = []
	for i,img in enumerate(images):
		hashlist.append(get_hash(path + img))
	return hashlist


def get_hash_video(path):
	scene_change = get_scene_images(path)
	name = path.split("/")[-1].split(".")[0]
	dire_name = "./" + name + "/"
	hashlist = get_hash_from_dir(dire_name)
	return hashlist, scene_change

def longest_common_subarray(l1, l2):
	subarray = []
	indices = []
	len1, len2 = len(l1), len(l2)
	for i in range(len1):
		for j in range(len2):
			temp = 0
			cur_array = []
			cur_indices = []
			# while ((i+temp < len1) and (j+temp < len2) and (l1[i+temp]-l2[j+temp])<=30):
			while ((i+temp < len1) and (j+temp < len2) and l1[i+temp] == l2[j+temp]):
				cur_array.append(l2[j+temp])
				cur_indices.append(j+temp)
				temp+=1
			if (len(cur_array) > len(subarray)):
				subarray = cur_array
				indices = cur_indices
	return subarray, indices

def get_time_string(tsecs):
	m, s = divmod(tsecs, 60)
	h, m = divmod(m, 60)
	h = str(int(h))
	m = str(int(m))
	s = str(int(s))
	h = "0"*(2 - len(h)) + h
	s = "0"*(2 - len(s)) + s
	m = "0"*(2 - len(m)) + m
	time_string = h + ":" + m + ":" + s
	return time_string


def main():
	# t1 = time()
	print ("1")
	l1, l2 = get_hash_video("./silicon1.mkv")
	# t2 = time()
	# print (len(l1), len(l2))
	# print (t2-t1)
	print ("2")
	l3, l4 = get_hash_video("./silicon2.mkv")
	# t3 = time()
	# print (len(l3), len(l4))
	# print (t3-t2)

	subarray, indices = longest_common_subarray(l1, l3)
	for i in indices:
		print (l4[i])

	print ("Last")

	try:
		end = indices[-1] + 1
		print (l4[end])
	except:
		pass

	# indices = common_elements(l1, l3)
	# for i in indices:
	# 	print (l4[i[0]], "sec", l2[i[1]])

main()
