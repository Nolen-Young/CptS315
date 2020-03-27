#!/usr/bin/env python
#Nolen Young, 11517296
#HW3

import numpy as np
import re

learningRate = 1
ITERATIONS = 20

def charRange(c1, c2):
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)

def sumWeight(dataPack, weight):

    label = '\n'
    yHatTemp = 0
    for c in charRange('a', 'z'):
        tempWeight = weight[c]
        yHat = np.dot(dataPack, tempWeight)
        
        if yHat > yHatTemp:
            label = c

    if  label == '\n':
        label = 'a'
    return label

def bianaryPerceptron(testData, testLabel, dataFile, labelsFile):
    stopWords = set()
    stopWordsFile = open("stoplist.txt", "r")
	
    f = open("output.txt", "a")
    f.write("[Binary Perceptron]\n")
	
    for line in stopWordsFile: # loop through and create a stop word set
        stopWords.add(line.strip('\n'))
	
	
    FEATURES = 0
    ITERATIONS = 20
    learningRate = 1
	
    cookieWords = set()
    data = open(testData, "r")
	
    # adds all the words to cookieWords
    for line in data:
        for word in line.split():
            if word not in stopWords:
                if word not in cookieWords:
                    cookieWords.add(word)
                    FEATURES += 1

    weight = np.zeros(FEATURES, np.int) 
    cookieWords = sorted(cookieWords)
    cookieData = list()
    cookieLabel = list()
    
    #loops through and pairs data to labels
    for lineData, lineLabel in zip(open(str(testData), "r"), open(str(testLabel), "r")):
        temp = list()
        for word in cookieWords:
            if word in lineData.split():
                temp.append(1)
            else:
                temp.append(0)
        
        temp2 = np.array(temp)
        cookieData.append(temp)
        cookieLabel.append(lineLabel.strip('\n'))

    N,d = np.shape(cookieData)
    trainLen = N
    trainingMistakes = list()

    #This is the machine learning loop
    for k in range(ITERATIONS):
        mistake = 0
        for j in range(len(cookieData)):
            x = cookieData[j]
            yHat = np.dot(x, weight) 
            correct_label = int(cookieLabel[j])

            if yHat > 0:
                yHat = 1
            elif yHat == 0:
                yHat = 0
            else:
                yHat = 0

            if int(yHat) != correct_label:
                mistake += 1
                weight = weight + learningRate * x
        trainingMistakes.append(mistake)
    
    cookieData = list()
    cookieLabel = list()
    
    # gather all of the testing data
    for lineData, lineLabel in zip(open(str(dataFile), "r"), open(str(labelsFile), "r")):
        temp = list()
        for word in cookieWords:
            if word in lineData.split():
                temp.append(1)
            else:
                temp.append(0)
        
        temp2 = np.array(temp)
        cookieData.append(temp)
        cookieLabel.append(lineLabel.strip('\n'))

    N,d = np.shape(cookieData)
    testLen = N
    testingMistakes = list()

    # Testing loop
    for k in range(ITERATIONS):
        mistake = 0
        for j in range(len(cookieData)):
            x = cookieData[j]
            yHat = np.dot(x, weight) 
            correct_label = int(cookieLabel[j])

            if yHat > 0:
                yHat = 1
            elif yHat == 0:
                yHat = 0
            else:
                yHat = 0

            if int(yHat) != correct_label:
                mistake += 1
                weight = weight + learningRate * x
        testingMistakes.append(mistake)
    
    i = 1
    for test, train in zip(testingMistakes,trainingMistakes):
        trainingAccuracy = (float(trainLen)-float(train))/float(trainLen)
        trainingAccuracy = trainingAccuracy * 100.00
        testingAccuracy = (float(testLen)-float(test))/float(testLen)
        testingAccuracy = testingAccuracy * 100.00
        f.write("iteration-%d: TrainMistakes:%s TrainAccuracy:%f TestMistakes:%s TestAccuracy:%f\n" %(i, train, trainingAccuracy, test, testingAccuracy))
        i += 1
    f.close()  

def multiclassPerceptron(trndata, testData):

    f = open("output.txt", "a")
    f.write("[Multi Class Perceptron]\n")
    
    FEATURES = 128
    ITERATIONS = 20
    learningRate = 1    
    trainingMistakes = list()
    weight = dict()
    
    # initiate weight
    for c in charRange('a', 'z'):
        weight[c]= (np.zeros(FEATURES, np.int) )

    
    dataFile= open(trndata)
    data = []
    
    #training loop
    for line in dataFile:
        templine = line.strip().split("\t")
        if templine[0] != '':
            binary = []
            
            for char in templine[1][2:]:
                binary.append(int(char))
        
            label = templine[2]
            dataPack = (binary, label)
            data.append(dataPack)


    for k in range(ITERATIONS):
        mistake = 0
        for item in data:
            dataPacket = item[0]
            dataLabel = item[1]
            tempLabel = sumWeight(dataPacket,weight)

            if  tempLabel!= dataLabel:
                
                weight[dataLabel] = weight[dataLabel] + (learningRate * dataPacket)
                weight[tempLabel] = weight[tempLabel] - (learningRate * dataPacket)
                mistake += 1
        trainingMistakes.append(mistake)
    trainLen = len(data)
    
    testingMistakes = list()
    dataFile= open(testData)
    
    #test loop
    data = []
    for line in dataFile:
        templine = line.strip().split("\t")
        if templine[0] != '':
            binary = []
            for char in templine[1][2:]:
                binary.append(int(char))
        
            label = templine[2]
            dataPack = (binary, label)
            data.append(dataPack)

    for k in range(ITERATIONS):
        mistake = 0
        for item in data:
            dataPacket = item[0]
            dataLabel = item[1]
            tempLabel = sumWeight(dataPacket,weight)
            
            if  tempLabel!= dataLabel:
                weight[dataLabel] = weight[dataLabel] + (learningRate * dataPacket)
                weight[tempLabel] = weight[tempLabel] - (learningRate * dataPacket)
                mistake += 1
        testingMistakes.append(mistake)
    testLen= len(data)
    
    #output
    i = 1
    for test, train in zip(testingMistakes,trainingMistakes):
        trainingAccuracy = (float(trainLen)-float(train))/float(trainLen)
        trainingAccuracy = trainingAccuracy * 100.00
        testingAccuracy = (float(testLen)-float(test))/float(testLen)
        testingAccuracy = testingAccuracy * 100.00
        f.write("iteration-%d: TrainMistakes:%s TrainAccuracy:%f TestMistakes:%s TestAccuracy:%f\n" %(i, train, trainingAccuracy, test, testingAccuracy))
        i += 1
    f.close()  

if __name__ == "__main__":
    f = open("output.txt", "w")
    f.write("Homework 3\n")
    f.close()  
    bianaryPerceptron("traindata.txt",  "trainlabels.txt", "testdata.txt", "testlabels.txt")
    multiclassPerceptron("ocr_train.txt", "ocr_test.txt")