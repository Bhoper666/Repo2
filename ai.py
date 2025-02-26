import turtle
import time

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")

# Create a turtle for the rectangle
rectangle_turtle = turtle.Turtle()
rectangle_turtle.shape("square")
rectangle_turtle.shapesize(stretch_wid=5, stretch_len=10)  # Adjust size as needed
rectangle_turtle.color("white")
rectangle_turtle.penup()
rectangle_turtle.goto(0, 0)

# Pause for 5 seconds
time.sleep(5)

# Transform the rectangle into a green circle
rectangle_turtle.shape("circle")
rectangle_turtle.shapesize(stretch_wid=2.5, stretch_len=2.5)  # Circle size 2 times smaller than the rectangle
rectangle_turtle.color("green")

# Keep the window open
turtle.done()
