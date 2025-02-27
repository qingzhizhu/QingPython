
#!/usr/bin/python
#coding=utf-8
#desc:....
#author:gengkun123@gmail.com

import os,sys
import webbrowser

DIR=os.getcwd()

def foo():
	a = webbrowser.load("https://classroom.udacity.com/nanodegrees/nd101-cn-advanced/parts/d0e8d7b2-a9bc-4eb2-b76e-bee3874c92a5")
	del
	print(a)

if __name__ == "__main__":
	# for arg in sys.argv:  
	# 	print(arg)

	print("file:", sys.argv[0])
	for i in range(1, len(sys.argv)):
		print("param:", i, sys.argv[i])

	foo()