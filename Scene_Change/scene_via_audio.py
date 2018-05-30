from pydub import AudioSegment
import subprocess
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np

file_input = "./videos/friends.mkv"
file_output = "friends.wav"

# command = "ffmpeg -i " + file_input +" -t 300 -codec:a pcm_s16le -ac 1 "+ file_output #converts the first 5 minutes of video file to wav output
# subprocess.call(command, shell=True)

read_audio = AudioSegment.from_wav("friends.wav")

time_dict = {}

for i in range(0, 300000, 3):
	print i
	t1 = i
	t2 = i+3
	audio_segment = read_audio[t1:t2]
	audio_segment.export("audio_segment.wav", format="wav")
	_, data = wav.read("audio_segment.wav")
	# fft_out = np.abs(fft(data))
	# print fft_out
	fft_out = np.abs(np.fft.rfft(data))
	# print fft_out2
	# break
	maxi = np.max(fft_out)
	mini = np.min(fft_out)
	var = np.var(fft_out)
	score = (maxi + mini)/var
	# print score
	if score>0.01:
		sec = i/1000
		time = str(int(sec/60))+" min: "+ str(int(sec%60)) + " sec"
		try:
			time_dict[time]+=1
		except:
			time_dict[time]=1
	print

print time_dict

# t1 = 0
# t2 = 12000

# newAudio = AudioSegment.from_wav("bbt.wav")
# newAudio = newAudio[t1:t2]
# newAudio.export('newSong.wav', format="wav") #Exports to a wav file in the current path

# rate, data = wav.read('newSong.wav')
# fft_out = fft(data)

# print np.var(fft_out)
# print np.var(np.abs(fft_out))

# print np.max(np.abs(fft_out))

# print np.abs(np.min(fft_out))
# print np.abs(np.max(fft_out))

# print fft_out



# def get_time_string(tsecs):
    
#     m, s = divmod(tsecs, 60)
#     h, m = divmod(m, 60)
#     h = str(int(h))
#     m = str(int(m))
#     s = str(int(s))
#     h = "0"*(2 - len(h)) + h
#     s = "0"*(2 - len(s)) + s
#     m = "0"*(2 - len(m)) + m
#     time_string = h + ":" + m + ":" + s
#     return time_string


# overlap = 0
# window = 2

# fs, frames = wav.read("bbt.wav")

# print fs
# print len(frames)
# start = 0
# i = window
# m = int(len(frames) / (window * fs) - 1) # As (k + 1)*window*fs < len(frames)
# print m
# n = np.fft.fftfreq(int(fs*window))[: fs // 2].shape[0] #Only real part
# n = n / 2 #Since we take only half of real part
# print n
# X = np.zeros((m, n), dtype=np.float32)
# print m, n

# k = 0
# print "fft"
# while ((i*fs) < len(frames)):
# 	# print i
# 	end = start + int(fs * window)
# 	x = np.array(frames[start:end], dtype=np.float32) + 0.0000001#To remove any zero errors
# 	# print len(x)
# 	magnitudes = np.abs(np.fft.rfft(x))[:fs / 4]
# 	# print len(magnitudes)
# 	# print len(X[k])
# 	# print k
# 	try:
# 		X[k] = np.copy(magnitudes)
# 	except:
# 		pass
# 	start += int(fs * (1 - overlap) * window)
# 	i += window
# 	k += 1

# print "fft done"
# freqs = np.abs(np.fft.fftfreq(n, 1.0/44100))
# times = []
# times_dic = {}
# print "scores"
# for i in range(m):
#     magnitudes = X[i, :]
#     val = (np.max(magnitudes) + np.min(magnitudes)) / (np.var(magnitudes))
#     val *= 100
    
#     print val
#     if val > 1:
#         ts = get_time_string(i * window)
#         try:
#             times_dic[ts] += 1
#         except:
#             times_dic[ts] = 0
# print
# print times_dic
# times = times_dic.keys()
# times.sort()
# for time in times:
#     if times_dic[time] == 0: #Occurred only once, very low chances of it being valid
#         del times_dic[time]
# times = times_dic.keys()
# times.sort()
# print times


