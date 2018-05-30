import subprocess

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



threshold = 0.35
input_file = "bbt2.avi"

# "ffmpeg -i bbt.avi -ss 0 -t 120 bbt.avi"

scenes = "ffmpeg -i " + input_file + '  -filter:v "select=' + "'gt(scene," + str(threshold) + ")'," + 'showinfo"  -f null  - 2>scenes3'
subprocess.call(scenes, shell = True)


scene_times = "grep showinfo scenes3 | grep 'pts_time:[0-9.]*' -o | grep '[0-9.]*' -o > scene_times3"
subprocess.call(scene_times, shell = True)

# print scene_change

file = open("scene_times3", "r")

timings = file.read()

file.close()

timings = timings.strip().split("\n")



timings = [float(i) for i in timings]

timings = list(set(timings))
timings.sort()

new_timings = []

for i in timings:
	z = get_time_string(i)
	if z not in new_timings:
		new_timings.append(z)

print len(new_timings)
for i in new_timings:
	print i 
# print


# final_timings = []

# i=0
# final_timings.append(timings[i])
# i+=1

# while i!=len(timings):
# 	if timings[i]<(final_timings[-1] + 5):
# 		i+=1
# 	else:
# 		final_timings.append(timings[i])
# 		i+=1


# print timings

# print final_timings


# print len(timings)
# for i in final_timings:
# 	print get_time_string(i)

# times = [timings[0]]

# for i in range(1, len(timings)):
# 	if timings[i]<(timings[i-1]+3):
# 		pass
# 	else:
# 		times.append(timings[i])

# print
# print len(times)
# for i in times:
# 	print get_time_string(i)


