#!/usr/bin/env python
"""
CptS_315 HW1
Nolen Kelly Young
11517296
READ ME:
I was able to get the program working for just pairs of items, but I was unable to get the 
program functioning for triples at a reasonable speed. I am turning this in for partial credit.
"""

import itertools
dataPath = "./hw1 test data.txt"
writePath = "./hw1 test results.txt"

def main():
	dataFile = open(dataPath, "r")
	#Find all frequent items
	frequentItems = FindFrequentItems(dataFile)
	dataFile = open(dataPath, "r")
	#find all frequent pairs
	frequentPairs = FindFrequentItemPairs(dataFile, frequentItems)
	# find and order by confidence value
	confidenceValues = CalculateConfidenceValues(frequentItems, frequentPairs)
	#write results
	writeFile = open(writePath, "w")
	writeFile.write("OUTPUT A\n")
	count = 0
	for item in confidenceValues:
		writeFile.write(item[0][0] + " " + item[0][1] + " " + str(item[1]) + "\n")
		if count == 4:
			break
		else: 
			count +=1

#Finds the frequent items in the file
def FindFrequentItems(dataFile):
	itemCounts = {}
	frequentItems = {}
	#keeps a count of each word, if the word has enough support then it is added to frequentItems to be returned
	for line in dataFile:
		for word in line.split():
			if word in itemCounts:
				itemCounts[word] += 1
			else:
				itemCounts[word] = 1
				
			if itemCounts[word] >= 100: #SUPPORT THRESHOLD
				if word in frequentItems:
					frequentItems[word] += 1
				else:
					frequentItems[word] = 100 #SUPPORT THRESHOLD
	
	return frequentItems

#Finds all pairs of frequent items
def FindFrequentItemPairs(dataFile, frequentItems):
	itemCounts = {}
	frequentItemPairs = {}
	words = []
	#searches line by line in the file to find pairs of frequent items
	for line in dataFile:
		words = line.split()
		for i in range (len(words)):
			for j in range(i+1, len(words)):
				#This disgusting block of if statements just counts item pairs, and if the pair has enough support its added to frequentItemPairs to be returned
				if words[i] in frequentItems and words[j] in frequentItems:
					if (words[i],words[j]) in itemCounts:
						itemCounts[(words[i],words[j])] += 1
						if itemCounts[(words[i],words[j])] >= 100:
							if (words[i],words[j]) in frequentItemPairs:
								frequentItemPairs[(words[i],words[j])] += 1
							elif (words[j],words[i]) in frequentItemPairs:
								frequentItemPairs[(words[j],words[i])] +=1
							else:
								frequentItemPairs[(words[i],words[j])] = 100
					elif (words[j],words[i]) in itemCounts:
						itemCounts[(words[j],words[i])] +=1
						if itemCounts[(words[j],words[i])] >= 100:
							if (words[i],words[j]) in frequentItemPairs:
								frequentItemPairs[(words[i],words[j])] += 1
							elif (words[j],words[i]) in frequentItemPairs:
								frequentItemPairs[(words[j],words[i])] +=1
							else:
								frequentItemPairs[(words[i],words[j])] = 100
					else:
						itemCounts[(words[i],words[j])] = 1
						
	return frequentItemPairs

#Calculate confidence values
def CalculateConfidenceValues(frequentItems, frequentPairs):
	confidenceValues = {}
	# Calculate all confidence values
	for pair in frequentPairs:
		confidenceValues[pair] = frequentPairs[pair] / frequentItems[pair[0]]
		confidenceValues[(pair[1], pair[0])] = frequentPairs[pair] / frequentItems[pair[1]]
	# sort the list and then reverse it so highest values are first
	sorted_by_value = sorted(confidenceValues.items(), key=lambda kv: kv[1])
	sorted_by_value.reverse()
	return sorted_by_value

if __name__ == "__main__":
	main()