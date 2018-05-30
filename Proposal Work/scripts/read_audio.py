import subprocess
import numpy as np
import scipy
import librosa
import matplotlib.pyplot as plt

file_input = "/path for/video file/"
file_output = "/path for/output audio file.wav/"

command = "ffmpeg -i " + file_input +" -t 300 -codec:a pcm_s16le -ac 1 "+ file_output #converts the first 5 minutes of video file to wav output
subprocess.call(command, shell=True)

x, sr = librosa.load(file_output)

rmse = librosa.feature.rmse(x)
rate = 300.0/rmse.shape[1]
time = [i*rate for i in range(1,rmse.shape[1]+1)] #get corresponding time values for frames
plt.figure(1)
plt.plot(time, rmse[0])
plt.show()

zcrs = librosa.feature.zero_crossing_rate(x)
plt.figure(2)
plt.plot(time, zcrs[0])
plt.show()

'''
Tried taking difference of above two values

diff = []
for i in range(len(zcrs[0])):
	z = rmse[0][i]-zcrs[0][i]
	if z>0:
		z=0
	diff.append(z)
plt.figure(3)
plt.plot(ind, diff)
plt.show()
'''
