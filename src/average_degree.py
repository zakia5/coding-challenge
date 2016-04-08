"""
Created on Thu Apr  7 18:24:56 2016

@author: zakia
"""
# example of program that calculates the degree of edge vertex
from sys import argv
import json
import itertools
from datetime import datetime 
from time import strptime
from collections import Counter

# Key: created at timestamp of tweet, Value: hastags in tweet
timeHashtagDict = dict()

#global list for current edges in graph
graphEdgesList = list()
# format the JSON timestamp in datetime standard format
def convert_time(timest):
	elements = timest.split(" ")
	year=int(elements[-1])
	month=int(strptime(elements[1],'%b').tm_mon)
	date=int(elements[2])
	time=elements[3].split(":")
	hour=int(time[0])
	minute=int(time[1])
	second=int(time[2])
	return datetime(year,month,date,hour,minute,second)

#function to check if the time difference between timestamps is less than 60 seconds
def isValidTimeDifference(timestamp1,timestamp2):
	difference = (timestamp2-timestamp1).total_seconds()	
	if difference < 60:
		return True
	return False

#function to get hashtags and created timestamp from tweet data
#return: list of hashtags in tweet and its create timestamp
def Hashtags_time(inputText):
	Hashtags = list()
	timest = ""
	jsonData = json.loads(inputText)
	#take all hashtags, make them lower case and remove duplicates
	if "entities" in jsonData:
		Entities = jsonData["entities"]
		if "hashtags" in Entities:
			hashtagList = Entities["hashtags"]
			if hashtagList:		
				Hashtags = [item['text'] for item in hashtagList]
				Hashtags = [tag.lower() for tag in Hashtags]
				Hashtags = list(set(Hashtags))
	#take created_at timestamp and convert into datetime format
	if "created_at" in jsonData:
		timest = jsonData["created_at"]
		timest = convert_time(timest)
	return Hashtags, timest

# Creating all the combinations of hash tags and sorted so as to avoid duplicated edge list
def Edge_list(Hashtags):
	Hashtags = sorted(set(Hashtags))
	return list(itertools.combinations(Hashtags, 2))

#function to remove invalid edges from graph
#return: updated graph
def evictInvalidEdges():
	global graphEdgesList
	global timeHashtagDict
	invalidTimestamps=[]
	#find invalid timestamps
	latestTimestamp = max(timeHashtagDict.keys())
	originalTimestamps=timeHashtagDict.keys()
	for timestamp in originalTimestamps:
		if not isValidTimeDifference(timestamp,latestTimestamp):
			#for each invalid tweet with respect to timestamp, find its edges and remove them from graph
			invalidHashtagsList=timeHashtagDict[timestamp]
			invalidEdges=Edge_list(invalidHashtagsList)
			graphEdgesList=list(set(graphEdgesList)-set(invalidEdges))
			invalidTimestamps.append(timestamp)
	#update global dictionary to store only the createDTTM and hashtags of valid tweets
	timeHashtagDict = dict( (k, v) for k,v in timeHashtagDict.items() if k not in invalidTimestamps)

# calculate  average degree of node 
def AvgNode():	
	global graphEdgesList
	uniqueNodesInGraphList=list()
	allNodesInEdges=list()
	nodeDegreeDict=dict()
	nodeDegreeList=list()
	allNodesInEdges=list(itertools.chain(*graphEdgesList))
	#find total nodes in graph
	uniqueNodesInGraphList=list(set(allNodesInEdges))
	totalNodesInGraph=len(uniqueNodesInGraphList)
	#find sum of degrees of all nodes and average degree
	nodeDegreeDict=Counter(allNodesInEdges)
	nodeDegreeList=nodeDegreeDict.values()
	sumNodeDegree=sum(nodeDegreeList)
	if totalNodesInGraph == 0:
		avgDeg = 0
	else:	
		avgDeg=sumNodeDegree/totalNodesInGraph
	return "%.2f" % avgDeg

#reads the input tweet file  and compute edges, graph and average degree of graph
#return: output file in specified format
def Caldegree_Graph(inputFile,outputFile):
        global timeHashtagDict	
        global graphEdgesList 	
        with open(inputFile, "r") as inFile, open(outputFile, "w") as outFile:
            for line in inFile:
			#for each tweet, compute and store hashtags and time, update graph with edges from new tweet's hashtags
			#and calculate average degree of graph
                Hashtags, timest = Hashtags_time(line)	
                if timest:
                    timeHashtagDict[timest]=Hashtags
                ## updated graph with new edges added to it and old edges removed
                if len(Hashtags)>=2:
                    edges=Edge_list(Hashtags)
                    graphEdgesList = list(set(graphEdgesList + edges))
                evictInvalidEdges()
                avgDegree=AvgNode()
                outFile.write(str(avgDegree)+'\n')
if __name__ == '__main__':
    if len(argv) == 3:   
        inputFile = argv[1]
        outputFile = argv[2]
        Caldegree_Graph(inputFile,outputFile)
  
