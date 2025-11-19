import pygame


class Paddle:
    # Sets the paddle movement speed in pixels per frame.
    VEL = 4

    # Defines the paddle dimensions.
    WIDTH = 20
    HEIGHT = 100

    # Initialises a paddle at position (x, y) and stores its original position.
    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y

    # Draws the paddle as a white rectangle on the given window surface.
    def draw(self, win):
        pygame.draw.rect(
            win, (255, 255, 255), (self.x, self.y, self.WIDTH, self.HEIGHT)
        )

    # Moves the paddle up or down by its velocity.
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    # Resets the paddle position back to its original coordinates.
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y