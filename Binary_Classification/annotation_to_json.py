import json

labels_file = open("annotation.txt", "r")
labels = labels_file.read()
labels = labels.strip().split("\n")

labels_dic = {}

for ele in labels:
	temp = ele.split(",")
	ele_dic = {}
	ele_dic["intro_start"] = temp[1]
	ele_dic["intro_end"] = temp[2]
	ele_dic["outro_start"] = temp[3]
	ele_dic["outro_end"] = temp[4]
	labels_dic[temp[0]] = ele_dic

data = json.dumps(labels_dic)


# print labels_dic

with open("annotation.json","w") as f:
  f.write(data)