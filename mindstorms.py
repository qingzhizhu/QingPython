import turtle

def draw_square(_turtle):
	for i in range(1,5):
		_turtle.forward(100)
		_turtle.right(90)

def draw_art():
	brad = turtle.Turtle()
	brad.shape("turtle")
	brad.color("yellow")
	brad.speed(2)

	total=12
	i=0
	while i<total:
		draw_square(brad)
		brad.right(30)
		i=i+1

	




window = turtle.Screen()
window.bgcolor("red")

draw_art()
window.exitonclick()