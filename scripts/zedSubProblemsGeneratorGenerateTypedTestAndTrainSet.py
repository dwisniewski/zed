__author__ = 'Pawel'

import sys
import random as rnd
import ntpath


src_file_name = ""

def getTypeMap(header):
    map = dict()
    i = 0
    for line in header:
        if "@attribute" in line:
            if "A FROM" in line:
                map[i] = "A FROM"
            if "A REPLY" in line:
                map[i] = "A REPLY"
            if "A SENT" in line:
                map[i] = "A SENT"
            if "A SUBJECT" in line:
                map[i] = "A SUBJECT"
            if "A TO " in line:
                map[i] = "A TO "
            if "A TYPE" in line:
                map[i] = "A TYPE"
            if "A WORD" in line:
                map[i] = "A WORD"
            i+=1
    return map

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def filterContent(type, typeMap, content):
    new_content = list()
    for line in content:
        if line[0] == '{':
            new_elements = list()
            line = line[1:-2]
            old_elements = line.split(',')
            for element in old_elements:
                #print typeMap
                pair = element.split(' ')
                if is_number(pair[1]):
                    #print pair
                    if typeMap.has_key(int(pair[0])):
                        if typeMap[int(pair[0])] == type:
                            new_elements.append(element)
                else:
                    new_elements.append(element)
            if (len(new_elements) > 1):
                new_elements = ",".join(new_elements)
                new_elements = '{' + new_elements + '}'
                new_content.append(new_elements)
    return new_content

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
typeMap = getTypeMap(header)
traintest = divideTrainTest(clusterData(data), 0.75)

#trainFile = open('train111.arff', 'w+')
src_file_name = ntpath.basename(sys.argv[1])
print src_file_name
testFileFrom = open('test_FROM_' + src_file_name, 'w+')
testFileReply = open('test_REPLY_' + src_file_name, 'w+')
testFileSent = open('test_SENT_' + src_file_name, 'w+')
testFileSubject = open('test_SUBJECT' + src_file_name, 'w+')
testFileTo = open('test_TO_' + src_file_name, 'w+')
testFileType = open('test_TYPE_' + src_file_name, 'w+')
testFileWord = open('test_WORD_' +src_file_name, 'w+')

trainFileFrom = open('train_FROM_' + src_file_name, 'w+')
trainFileReply = open('train_REPLY_' + src_file_name, 'w+')
trainFileSent = open('train_SENT_' + src_file_name, 'w+')
trainFileSubject = open('train_SUBJECT_' + src_file_name, 'w+')
trainFileTo = open('train_TO_' + src_file_name, 'w+')
trainFileType = open('train_TYPE_' + src_file_name, 'w+')
trainFileWord = open('train_WORD_' +src_file_name, 'w+')

for line in header:
    testFileFrom.write(line + "\n")
    testFileReply.write(line + "\n")
    testFileSent.write(line + "\n")
    testFileSubject.write(line + "\n")
    testFileTo.write(line + "\n")
    testFileType.write(line + "\n")
    testFileWord.write(line + "\n")

print "creating test set"
for key in traintest:
    fromContent = filterContent("A FROM", typeMap, traintest[key]["test"])
    replyContent = filterContent("A REPLY" , typeMap, traintest[key]["test"])
    sentContent = filterContent("A SENT", typeMap, traintest[key]["test"])
    subjectContent = filterContent("A SUBJECT", typeMap, traintest[key]["test"])
    toContent = filterContent("A TO ", typeMap, traintest[key]["test"])
    typeContent = filterContent("A TYPE", typeMap, traintest[key]["test"])
    wordContent = filterContent("A WORD", typeMap, traintest[key]["test"])

    for line in fromContent:
        testFileFrom.write(line + "\n")
    for line in replyContent:
        testFileReply.write(line + "\n")
    for line in sentContent:
        testFileSent.write(line + "\n")
    for line in subjectContent:
        testFileSubject.write(line + "\n")
    for line in toContent:
        testFileTo.write(line + "\n")
    for line in typeContent:
        testFileType.write(line + "\n")
    for line in wordContent:
        testFileWord.write(line + "\n")
print "creating training set"
for key in traintest:
    fromContent = filterContent("A FROM", typeMap, traintest[key]["train"])
    replyContent = filterContent("A REPLY" , typeMap, traintest[key]["train"])
    sentContent = filterContent("A SENT", typeMap, traintest[key]["train"])
    subjectContent = filterContent("A SUBJECT", typeMap, traintest[key]["train"])
    toContent = filterContent("A TO ", typeMap, traintest[key]["train"])
    typeContent = filterContent("A TYPE", typeMap, traintest[key]["train"])
    wordContent = filterContent("A WORD", typeMap, traintest[key]["train"])

    for line in fromContent:
        trainFileFrom.write(line + "\n")
    for line in replyContent:
        trainFileReply.write(line + "\n")
    for line in sentContent:
        trainFileSent.write(line + "\n")
    for line in subjectContent:
        trainFileSubject.write(line + "\n")
    for line in toContent:
        trainFileTo.write(line + "\n")
    for line in typeContent:
        trainFileType.write(line + "\n")
    for line in wordContent:
        trainFileWord.write(line + "\n")

        #trainFile.write(line + "\n")

        #testFile = open('test111.arff', 'w+')
        #for line in header:
        #	testFile.write(line + "\n")
        #for key in traintest:
        #	for line in traintest[key]["test"]:
        #		testFile.write(line + "\n")