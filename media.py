#!/usr/bin/python
#coding=utf-8
#desc:电影demo class
#author:gengkun123@gmail.com

import webbrowser

class Movie():
	"""this is a desc from movie"""
	def __init__(self, title, storyline, posterImge, trailer_youtube):
		self.title = title
		self.storyline = storyline
		self.poster_image_url = posterImge
		self.trailer_youtube_url = trailer_youtube

	def show_trailer(self):
		webbrowser.open(self.trailer_youtube_url)	

