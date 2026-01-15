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
        # Track turtle states
        state_stack = []

        # Initialize bounds at starting position
        x0, y0 = self.turtle.pos()
        xmin = xmax = x0
        ymin = ymax = y0

        for i, task in enumerate(code):

            # Follow turtle during rendering
            if i % 2000 == 0:
                self.follow_turtle(self.turtle)

            if task == 'F':
                # Randomize color + pen size
                color = (
                    random.random(),
                    random.random(),
                    random.random()
                )
                self.turtle.pencolor(color)
                self.turtle.pensize(random.random() * 20)

                self.turtle.forward(self.distance)

                # Update bounds
                x, y = self.turtle.pos()
                xmin = min(xmin, x)
                xmax = max(xmax, x)
                ymin = min(ymin, y)
                ymax = max(ymax, y)

            elif task == 'B':
                self.turtle.backward(self.distance)
                x, y = self.turtle.pos()
                xmin = min(xmin, x)
                xmax = max(xmax, x)
                ymin = min(ymin, y)
                ymax = max(ymax, y)

            elif task == '[':
                state_stack.append((self.turtle.pos(), self.turtle.heading()))

            elif task == ']':
                pos, heading = state_stack.pop()
                self.turtle.up()
                self.turtle.setpos(pos)
                self.turtle.setheading(heading)
                self.turtle.down()

            elif task == '+':
                self.turtle.right(self.theta)

            elif task == '-':
                self.turtle.left(self.theta)

        # Zoom out before saving
        width = xmax - xmin
        height = ymax - ymin
        pad = 0.1 * max(width, height)

        turtle.setworldcoordinates(
            xmin - pad, ymin - pad,
            xmax + pad, ymax + pad
        )

        turtle.update()

        screen = turtle.getscreen()
        screen.getcanvas().postscript(file="output.eps")

        img = Image.open("output.eps")
        img.save("output.png", "png")

        turtle.mainloop()