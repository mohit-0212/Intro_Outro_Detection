import cv2
import numpy as np
import matplotlib.pyplot as plt

vid_frame = cv2.VideoCapture('videos/bbt.avi')

length = vid_frame.get(cv2.CAP_PROP_FRAME_COUNT)
fps = vid_frame.get(cv2.CAP_PROP_FPS)

num_frames = int(fps*600)
print(num_frames)

# time = [i/fps for i in range(1,num_frames+1)]

correlation = []
time = []

# cur_hist = None
# prev_hist = None

cur_img = None
prev_img = None

diff = {}

for i in range(0, num_frames):
	print(i)
	success, image = vid_frame.read()
	if i%1 == 0:
		if success:
			# image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
			# hist = cv2.calcHist([image],[0],None,[256],[0,256])
			cur_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			# cur_hist = cv2.calcHist([image], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
			if i==0:
				pass
			else:
				absdif = cv2.absdiff(cur_img, prev_img).sum()
				# print absdif
				# correlation.append(cv2.compareHist(cur_hist, prev_hist, cv2.HISTCMP_CORREL))
				# time.append(i/fps)
				try:
					diff[int(absdif)]+=1
				except:
					diff[int(absdif)] = 1
			prev_img = cur_img
			# prev_hist = cur_hist

# plt.plot(correlation)
# plt.show()
x = []
y = []


for i in sorted(diff)[0:500]:
	x.append(i)
	y.append(diff[i])
print x
print y
plt.plot(x,y)
plt.show()

# scene_change = np.argpartition(np.array(correlation), 10)[:10]

# for i in scene_change:
# 	change_time = str(int(time[i]/60))+" min: "+ str(int(time[i]%60)) + " sec" #gives the intro end time in the format x min: y sec
# 	print(change_time)
