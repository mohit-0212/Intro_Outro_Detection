import cv2
import numpy as np
import matplotlib.pyplot as plt

# vid_frame = cv2.VideoCapture('/path for/video file/')
vid_frame = cv2.VideoCapture('videos/breakingbad.mkv')

length = vid_frame.get(cv2.CAP_PROP_FRAME_COUNT)
fps = vid_frame.get(cv2.CAP_PROP_FPS)

num_frames = int(fps*300) #number of frames in first 5 minutes

time = [i/fps for i in range(1,num_frames+1)]
intensity = []

cnt = 0

for i in range(num_frames):
	success, image = vid_frame.read()
	cv2.imwrite("frames/"+str(cnt)+".jpg",image)
	cnt+=1
	image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	if success:
		total = np.sum(np.sum(image, axis = 0))
		intensity.append(total/(image.shape[0]*image.shape[1]))

vid_seq = []
for i in range(len(intensity)):
	if time[i]>=15:
		vid_seq.append(intensity[i])
	else:
		vid_seq.append(255) #max intensity value appended for the first 15 seconds to ignore any initial black screens

black_index = np.argpartition(np.array(vid_seq), 1)[:1][0]

time = str(int(time[black_index]/60))+" min: "+ str(int(time[black_index]%60)) + " sec" #gives the intro end time in the format x min: y sec
print time

# plt.plot(time, intensity)
# plt.show()
