from argparse import ArgumentParser
import os
import glob
import imagehash
from PIL import Image
import subprocess
import shutil
import copy


def get_hash(path):
	return imagehash.phash(Image.open(path))

def get_hash_from_dir(path):
	images = os.listdir(path)
	images.sort()
	hashlist = []
	for i,img in enumerate(images):
		hashlist.append(get_hash(os.path.join(path, img)))
	return hashlist, images

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

def get_scene_transitions(path, threshold):
	th = threshold
	end_time = 360 #in seconds (can be put in arguments as well)

	name, ext = os.path.splitext(path)
	# print (name)

	if os.path.exists(name):
		shutil.rmtree(name)
	os.mkdir(name)

	input_file = path

	scenes = "ffmpeg -i " + '"' + input_file + '"' + " -ss 0 -to " + str(end_time) + ' -vf  "select=' + "'gt(scene," + str(th) + ")'," + 'showinfo" -vsync vfr "' + name + '/' + '"%04d.jpg>scenes 2>&1'
	# print (scenes)
	subprocess.call(scenes, shell = True)

	file = open("scenes", "r")
	out = file.read()
	file.close()
	times = get_timings(out)
	os.remove("./scenes")

	return times

def get_hash_video(path, threshold):
	scene_transitions = get_scene_transitions(path, threshold)
	name, ext = os.path.splitext(path)
	hashlist, images = get_hash_from_dir(name)
	if os.path.exists(name):
		shutil.rmtree(name)
	return hashlist, scene_transitions

#Methods

#(1) All common matches

def common_elements(list1, list2):
	common = []
	for i, element in enumerate(list1):
		# if element in list2:
			# common.append(element)
		try:
			ind = list2.index(element)
			common.append((i, ind))
		except:
			pass
	return common

#(2) Longest continuos match

def longest_common_subarray(l1, l2):
	subarray = []
	indices = []
	len1, len2 = len(l1), len(l2)
	for i in range(len1):
		for j in range(len2):
			temp = 0
			cur_array = []
			cur_indices = []
			while ((i+temp < len1) and (j+temp < len2) and (l1[i+temp]-l2[j+temp])<=30): #hamming distance
			# while ((i+temp < len1) and (j+temp < len2) and l1[i+temp] == l2[j+temp]):
				cur_array.append(l2[j+temp])
				cur_indices.append((i+temp, j+temp))
				temp+=1
			if (len(cur_array) > len(subarray)):
				subarray = cur_array
				indices = cur_indices
	# return subarray, indices
	return indices


def gen_timings_processed(videos_process, threshold, method):
	intro_times = []
	hash_prev, scene_prev = get_hash_video(videos_process[0], threshold)
	print(0)
	for i in range(1, len(videos_process)):
		hash_cur, scene_cur = get_hash_video(videos_process[i], threshold)
		if method == "all_match":
			indices = common_elements(hash_prev, hash_cur)
			
			intro_start_prev = scene_prev[indices[0][0]]
			intro_start_cur = scene_cur[indices[0][1]]
			
			intro_end_prev = scene_prev[indices[-1][0] + 1]
			intro_end_cur = scene_cur[indices[-1][1] + 1]

			if len(intro_times)==0:
				time_string = str(intro_start_prev) + " " + str(intro_end_prev) + " 0" #cut in edl files
				intro_times.append(time_string)

			time_string = str(intro_start_cur) + " " + str(intro_end_cur) + " 0" #cut in edl files
			intro_times.append(time_string)
		elif method == "longest_common":
			indices = longest_common_subarray(hash_prev, hash_cur)
			
			intro_start_prev = scene_prev[indices[0][0]]
			intro_start_cur = scene_cur[indices[0][1]]
			
			intro_end_prev = scene_prev[indices[-1][0] + 1]
			intro_end_cur = scene_cur[indices[-1][1] + 1]

			if len(intro_times)==0:
				time_string = str(intro_start_prev) + " " + str(intro_end_prev) + " 0" #cut in edl files
				intro_times.append(time_string)

			time_string = str(intro_start_cur) + " " + str(intro_end_cur) + " 0" #cut in edl files
			intro_times.append(time_string)
		
		hash_prev = hash_cur
		scene_prev = scene_cur
		
		print(i)

	return intro_times


def create_edl(videos, timings):
	for i,file in enumerate(videos):
		filename, file_extension = os.path.splitext(file)
		suffix = '.edl'
		edl_file = filename + suffix
		f = open(edl_file, "w")
		f.write(timings[i])
		f.close()


def generate(path, threshold, method, force):
	files = os.listdir(path)
	all_files = [os.path.join(path, i) for i in files]

	#get the video files
	videos = []
	for ext in ('*.mp4', '*.mkv', '*.avi', '*.mov', '*.wmv'):	#video formats - extendable
		videos.extend(glob.glob(os.path.join(path, ext)))
	# print(videos)

	#if there is only 1 video in the directory
	if len(videos)==1:
		print("Add atleast 1 more video of the TV show to the directory for processing.")
		exit()

	#get videos which don't have a skip timings file (currently edl) according to --force parameter
	videos_process = []
	if force is False:
		for file in videos:
			filename, file_extension = os.path.splitext(file)
			suffix = '.edl'
			if (filename + suffix) not in all_files:
				videos_process.append(file)
	else:
		videos_process = copy.deepcopy(videos)
	# print(videos_process)

	if len(videos_process)==1:
		vid = videos_process[0]
		videos.sort() #basic ordering for videos by sorting based on season and episode
		try:
			comp_vid = videos[videos.index(vid) - 1]
		except:
			comp_vid = videos[videos.index(vid) + 1]
		intro_times = gen_timings_processed([comp_vid, vid], threshold, method)
		create_edl([vid], [intro_times[1]])
	else:
		videos_process.sort() #basic ordering for videos by sorting based on season and episode
		intro_times = gen_timings_processed(videos_process, threshold, method)
		create_edl(videos_process, intro_times)

	print("Timing files created.")

def main():
	argparse = ArgumentParser()
	argparse.add_argument('--path', '-p', type=str, help='TV show directory path')
	argparse.add_argument('--threshold', '-t', type=str, help='Threshold for scene change detection(default=0.35)', default='0.35')
	argparse.add_argument('--method', '-m', type=str, help='Method used for timings generation (all_match or longest_common)', default='all_match')
	argparse.add_argument('--force', action='store_true', help='Process all videos in the directory')
	args = argparse.parse_args()

	if args.path is None:
		print("Enter a directory path.")
		exit()
	else:
		if not os.path.exists(args.path):
			print ("TV show directory: " + args.path + " not found.")
			exit()
		else:
			if not os.path.isdir(args.path):
				print ("Path: " + args.path + " is not a directory.")	
				exit()

	if args.method!="all_match" and args.method!="longest_common":
		print("Enter correct method: (1) all_match (2) longest_common")
		exit()

	# print(args.path)
	# print(args.threshold)
	# print(args.method)
	# print(args.force)

	generate(args.path, args.threshold, args.method, args.force)



if __name__ == '__main__':
  main()