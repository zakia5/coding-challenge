"""
Created on Thu Apr  7 18:24:56 2016

@author: zakia
"""
# Program that calculates the number of tweets cleaned
from sys import argv
import json
Counter = 0 #counter for unicode characters

#python escape sequences to remove from tweets
escapes=["\\","\a","\b","\r","\n","\f","\t","\v"]

#removes non-ascii characters and escape sequences from string
#return: tweet text after removing unicode characters
def cleanEscapes(text):
	global escapes
	global Counter
	UnicodeFlag=False
	result=""
	#for each tweet, clean its text to remove unicode characters
	for i in text:
		if ord(i) < 128:
			if i not in escapes:
				result+=i
		else:
			UnicodeFlag=True
	#if unicode characters in tweet increment global counter
	if UnicodeFlag:
		 Counter+=1	
	return result

#extraction of timestamp, tweet text from json.
#return: Text and timest
def Text_Time(inputText):
	Text=""
	timest=""
	jsonData = json.loads(inputText)
	if "text" in jsonData:
		Text = jsonData["text"]
		Text = cleanEscapes(Text)
	if "created_at" in jsonData:
		timest = jsonData["created_at"]
	return Text, timest

#read, clean escape sequences and unicode characters and count tweets with unicode
# write this information after cleaning
def cleanTweets(inputFile,outputFile):
	global Counter
	with open(inputFile, "r") as inFile, open(outputFile, "w") as outFile:
		for line in inFile:
			#write each  cleaned text, time  in output file
			Text, timest = Text_Time(line)
			outFile.write(Text + " " + "(timestamp:" + " " + timest + ")" +"\n")
		outFile.write("\n")
		# write the number of tweets with unicode-characters 
		outFile.write(str(Counter) + " tweets contained unicode.")

if __name__ == '__main__':
    if len(argv) == 3:
        inputFile = argv[1]
        outputFile = argv[2]
        cleanTweets(inputFile,outputFile)
        print(Counter)  