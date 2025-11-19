import pygame
import math
import random


class Ball:
    # Sets the maximum speed for the ball.
    MAX_VEL = 5

    # Sets the radius of the ball in pixels.
    RADIUS = 7

    # Initialises the ball at position (x, y) with a random starting velocity.
    def __init__(self, x, y):
        # Stores the current and original positions so the ball can be reset later.
        self.x = self.original_x = x
        self.y = self.original_y = y
        
        # Chooses a random launch angle between -30 and 30 degrees, avoiding 0 so the ball never starts perfectly horizontal.
        angle = self._get_random_angle(-30, 30, [0])

        # Randomly decides whether the ball starts moving left or right.
        pos = 1 if random.random() < 0.5 else -1

        # Calculates the initial x and y velocity using the angle.
        self.x_vel = pos * abs(math.cos(angle) * self.MAX_VEL)
        self.y_vel = math.sin(angle) * self.MAX_VEL

    # Generates a random angle (in radians) between min_angle and max_angle (degrees),
    # excluding any angles that match the ones in the `excluded` list.
    def _get_random_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle

    # Draws the ball on the pygame window surface.
    def draw(self, win):
        pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), self.RADIUS)

    # Updates the ball’s position based on its current velocity.
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    # Resets the ball back to the centre with a fresh random direction.
    def reset(self):
        # Restores the original starting position.
        self.x = self.original_x
        self.y = self.original_y

        # Chooses a new random angle and recalculates velocity.
        angle = self._get_random_angle(-30, 30, [0])
        x_vel = abs(math.cos(angle) * self.MAX_VEL)
        y_vel = math.sin(angle) * self.MAX_VEL

        # Applies the new velocity, flipping the horizontal direction.
        self.x_vel = -x_vel
        self.y_vel = y_vel