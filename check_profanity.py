#!/usr/bin/python
#coding=utf-8
#desc:检查是否有脏话, python2
#author:gengkun123@gmail.com

import os,sys
import urllib

DIR=os.getcwd()

def check_profanity(text):
	connection = urllib.urlopen("http://www.wdylike.appspot.com/?q="+text)
	output = connection.read()
	print(output)
	connection.close()
	if "true" in output:
		print("Profanity Alert! 有敏感词")
	elif "false" in output:
			print("OK！this document has no curse words.")
	else:
		print("Could not scan the document properly.")



def read_text():
	quotes = open(DIR+"/movie_quotes.txt")
	contents = quotes.read()
	#print(contents)
	quotes.close()
	check_profanity(contents)


if __name__ == "__main__":
	# for arg in sys.argv:  
	# 	print(arg)

	print("file:", sys.argv[0])
	for i in range(1, len(sys.argv)):
		print("param:", i, sys.argv[i])

	read_text()
