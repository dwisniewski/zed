import sys
import random as rnd

def intToBinary(v):
	result = []
	while v > 0:
		result.append(v % 2)
		v /= 2

	reversed_result = []
	for i in range(len(result)):
		reversed_result.append(result[len(result)-i-1])
	return reversed_result


def getDataPartOfArff(path):
	f = open(path, 'r')
	result = []
	start = False
	for line in f:
		l = line.strip()
		if len(l) > 0:
			if start == True:
				result.append(l)
			if l == '@data':
				start = True
			
	return result


def getHeaderPartOfArff(path):
	f = open(path, 'r')
	result = []
	for line in f:
		l = line.strip()
		if len(l) > 0:
			if l == '@data':
				result.append(l)
				break
			else:
				result.append(l)
	return result

def getClassDistribution(data):
	dist = dict()
	for item in data:
		s = item.split(",")
		cl = s[-1].split(" ")[1][:-1]
		if cl in dist.keys():
			dist[cl] += 1
		else:
			dist[cl] = 1
	return dist

def clusterData(data):
	clusters = dict()
	for item in data:
		s = item.split(",")
		cl = s[-1].split(" ")[1][:-1]
		if cl in clusters.keys():
			clusters[cl].append(item)
		else:
			clusters[cl] = [item]
	return clusters

def divideTrainTest(clusters, training_fraction):
	traintest = dict()
	for key in clusters.keys():
		cluster_size = len(clusters[key])
		indices = rnd.sample(range(cluster_size), cluster_size)
		traintest[key] = dict()
		traintest[key]["train"] = []
		traintest[key]["test"] = []

		for i in indices[:int(training_fraction*cluster_size)]:
			traintest[key]["train"].append(clusters[key][i])
		for i in indices[int(training_fraction*cluster_size):]:
			traintest[key]["test"].append(clusters[key][i])

	return traintest

header = getHeaderPartOfArff(sys.argv[1])
data = getDataPartOfArff(sys.argv[1])

traintest = divideTrainTest(clusterData(data), 0.75)

#trainFile = open('train111.arff', 'w+')
trainFileFrom = open('train111_FROM.arff', 'w+')
trainFileReply = open('train111_REPLY.arff', 'w+')
trainFileSent = open('train111_SENT.arff', 'w+')
trainFileSubject = open('train111_SUBJECT.arff', 'w+')
trainFileTo = open('train111_TO.arff', 'w+')
trainFileType = open('train111_TYPE.arff', 'w+')
trainFileWord = open('train111_WORD.arff', 'w+')

for line in header:
	trainFileFrom.write(line + "\n")
	trainFileReply.write(line + "\n")
	trainFileSent.write(line + "\n")
	trainFileSubject.write(line + "\n")
	trainFileTo.write(line + "\n")
	trainFileType.write(line + "\n")
	trainFileWord.write(line + "\n")

for key in traintest:
	for line in traintest[key]["train"]: # zeby zrobic ograniczenie zbioru testowego do 50% zmien na for line in traintest[key]["train"][:len(traintest[key]["train"])/2]
		if line.contains("A FROM"):
			trainFileFrom.write(line + "\n")
		if line.contains("A REPLY"):
			trainFileReply.write(line + "\n")
		if line.contains("A SENT"):
			trainFileSent.write(line + "\n")
		if line.contains("A SUBJECT"):
			trainFileSubject.write(line + "\n")
		if line.contains("A TO "):
			trainFileTo.write(line + "\n")
		if line.contains("A TYPE"):
			trainFileType.write(line + "\n")
		if line.contains("A WORD"):
			trainFileWord.write(line + "\n")
		#trainFile.write(line + "\n")


#testFile = open('test111.arff', 'w+')
#for line in header:
#	testFile.write(line + "\n")
#for key in traintest:
#	for line in traintest[key]["test"]:
#		testFile.write(line + "\n")