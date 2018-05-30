import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_ssim

vid_frame = cv2.VideoCapture('/path for/video file/')
cover = cv2.cvtColor(cv2.imread('/path for/cover image/'), cv2.COLOR_BGR2GRAY)

length = vid_frame.get(cv2.CAP_PROP_FRAME_COUNT)
fps = vid_frame.get(cv2.CAP_PROP_FPS)

num_frames = int(fps*300) #number of frames in first 5 minutes

scores = []
time = []

resized = False

for i in range(num_frames):
	success, image = vid_frame.read()
	image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

	if not resized:
		height, width = image.shape[:2]
		cover = cv2.resize(cover,(width, height), interpolation = cv2.INTER_CUBIC) #resizes the cover image to the video frame size, performed only once
		resized = True

	if success and (i%int(fps)==0): #to check the frame every second
		print(i)
		score, _ = compare_ssim(image, cover, full=True) #similarity check between two images using the inbuilt skimage function
		scores.append(score)
		time.append(i/fps)

# plt.plot(scores) #to check the trend of scores
# plt.show()

maximum_score = np.argmax(np.array(scores))
intro_end = str(int(time[maximum_score]/60))+" min: "+ str(int(time[maximum_score]%60)) + " sec"
print(intro_end)

