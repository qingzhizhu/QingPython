#!/usr/bin/python
#coding=utf-8
#desc:....
#author:gengkun123@gmail.com

import os,sys

DIR=os.getcwd()

def foo():
	print("中文,Done!")


if __name__ == "__main__":
	# for arg in sys.argv:  
	# 	print(arg)

	print("file:", sys.argv[0])
	for i in range(1, len(sys.argv)):
		print("param:", i, sys.argv[i])

	foo()
