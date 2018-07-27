#!/usr/bin/python
#coding=utf-8
#desc: 继承demo
#author:gengkun123@gmail.com

import os,sys

DIR=os.getcwd()

class Parent():
	def __init__(self, last_name, eye_color):
		self.last_name = last_name
		self.eye_color = eye_color

class Child(Parent):
	"""docstring for Child"""
	def __init__(self, last_name, eye_color, number_of_toys):
		# super(Parent, self).__init__(last_name, eye_color)
		Parent.__init__(self, last_name, eye_color)
		self.number_of_toys = number_of_toys 
	
if __name__ == "__main__":
	# for arg in sys.argv:  
	# 	print(arg)

	print("file:", sys.argv[0])
	for i in range(1, len(sys.argv)):
		print("param:", i, sys.argv[i])

	son1 = Child("son_qq", "black", 10)
	print(son1.last_name)
	print(son1.number_of_toys)