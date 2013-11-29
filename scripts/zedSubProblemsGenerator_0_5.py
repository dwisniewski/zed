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

trainFile = open('train111_0_5.arff', 'w+')
for line in header:
	trainFile.write(line + "\n")
for key in traintest:
	for line in traintest[key]["train"][:len(traintest[key]["train"])/2]: # zeby zrobic ograniczenie zbioru testowego do 50% zmien na for line in traintest[key]["train"][:len(traintest[key]["train"])/2]
		trainFile.write(line + "\n")


testFile = open('test111_0_5.arff', 'w+')
for line in header:
	testFile.write(line + "\n")
for key in traintest:
	for line in traintest[key]["test"][:len(traintest[key]["test"])/2]:
		testFile.write(line + "\n")