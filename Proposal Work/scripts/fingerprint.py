#After setting up, dejavu locally on my machine
#Credits and Reference: https://github.com/worldveil/dejavu
import warnings
import json
import subprocess
import moviepy.editor as mp

warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer

# load config from a JSON file (or anything outputting a python dictionary)
with open("dejavu.cnf.SAMPLE") as f:
	config = json.load(f)

conf_scores = []

if __name__ == '__main__':
	djv = Dejavu(config) # create a Dejavu instance
	djv.fingerprint_directory("mp3", [".mp3"]) # Fingerprints all the mp3's in the directory given
	for i in range(0,300,6): #checks for audio in first 5 minutes with 5-6 second audio taken at a time
		clip = mp.VideoFileClip("your/video/clip").subclip(i,i+5) #extract the subclip
		clip.audio.write_audiofile("output/audio/file")
		song = djv.recognize(FileRecognizer, "output/audio/file") #to recognize the extracted audio file
		print "Recognized: %s\n" % song['song_name'], song['confidence'] #name of recognized song with confidence
		conf_scores.append(song['confidence'])

print (conf_scores)