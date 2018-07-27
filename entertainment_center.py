#!/usr/bin/python
#coding=utf-8
#desc:电影demo
#author:gengkun123@gmail.com

import os,sys
import media
import fresh_tomatoes

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
	s1 = media.Movie("tile1", "storeline", "img.png", "url")
	print(s1.title)



	toy_story=media.Movie("ToyStory","Astoryofaboyandhistoysthatcometolife",
	"http://upload.wikimedia.org/wikipedia/en/l/13/Toy_Story.jpg",
	"http://www.youtube.com/watch?v=vwyZH85NQC4M")
	#print(toy_story.storyline)
	avatar=media.Movie("Avatar","Amarineonanalienplanet",
	"http://upload.wikimedia.0rg/wikipedia/id/b/bO/Avatar-Teaser-Poster.jpg",
	"http://www.youtube.com/watch?v=-9ceBgWV8io")
	school_of_rock=media.Movie("SchoolofRock","Storyline",
	"http://upl0ad.wikimedia.0rg/wikipedia/en/l/ll/Sch00l_0f_R0ck_P0ster.jpg",
	"http://www.youtube.com/watch?v=3PsUJFEBC74M")
	ratatouille=media.Movie("Ratatouille11","Storyline",
	"http://upload.wikimedia.org/wikipedia/en/5/50/RatatouillePoster.jpg",
	"http://www.youtube.com/watch?v=c3sBBRxDAqk")
	midnight_in_paris=media.Movie("MidnightinParis","Storyline",
	"http://upload.wikimedia.org/wikipedia/en/9/9f^Midnight_in_Paris_Poster.jpg",
	"http://www.youtube.com/watch?v=atLg2wQQxvU")
	hunger_games=media.Movie("HungerGames","Storyline",
	"http://upload.wikimedia.org/wikipedia/en/4/42/HungerGamesPoster.jpg",
	"http://www.youtube.com/watch?v=PbA63a7H0boM")

	movies = [toy_story, avatar, school_of_rock, ratatouille, midnight_in_paris, hunger_games]
	# fresh_tomatoes.open_movies_page(movies)
	print(media.Movie.__doc__)

	#hunger_games.show_trailer()
	print("done!")
