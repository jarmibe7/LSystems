"""
Turtle rendering for 2D LSystems
"""
import turtle
from PIL import Image
import random

class RenderLSystem2D:
    """
    Render a 2D LSystem with a simulated turtle
    """
    def __init__(self, distance, theta, update_freq=0):
        # Setup for drawing
        window = turtle.Screen()
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        turtle.mode("logo")
        self.turtle.hideturtle()

        # screen.tracer(x) speeds up rendering by skipping frames
        turtle.tracer(update_freq)

        # Move turtle to left side of screen
        self.turtle.up()
        self.turtle.back(300)
        self.turtle.down()

        # Record distance and angle
        self.distance = distance
        self.theta = theta

    def follow_turtle(self, t):
        x, y = t.pos()
        half_width = 300
        half_height = 300
        turtle.setworldcoordinates(
            x - half_width, y - half_height,
            x + half_width, y + half_height
        )

    def draw(self, code):
        # Render a 2DLsystem
        state_stack = []

            

        for i, task in enumerate(code):
            if i % 1000 == 0:   # update camera every 20 steps
                self.follow_turtle(self.turtle)
            if task == 'F':
                color = (
                    random.random(),
                    random.random(),
                    random.random()
                )
                size = random.random()*80
                self.turtle.pensize(size)
                self.turtle.pencolor(color)
                self.turtle.forward(self.distance)
            elif task == 'B':
                self.turtle.backward(self.distance)
            elif task == '[':
                state = (self.turtle.pos(), self.turtle.heading())
                state_stack.append(state)
            elif task == ']':
                state = state_stack.pop()
                self.turtle.setpos(state[0])
                self.turtle.setheading(state[1])
            elif task == '+':
                self.turtle.right(self.theta)
            elif task == '-':
                self.turtle.left(self.theta)

        ts = turtle.getscreen()
        # Save to EPS + PNG and run render
        ts.getcanvas().postscript(file="output.eps")
        img = Image.open('output.eps')
        img.save('output.png', 'png')
        turtle.mainloop()