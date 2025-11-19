from .paddle import Paddle
from .ball import Ball
import pygame
import random
pygame.init()


class GameInformation:
    # Stores summary information about the current state of a game round.
    def __init__(self, left_hits, right_hits, left_score, right_score):
        # Tracks how many times the left paddle has hit the ball.
        self.left_hits = left_hits

        # Tracks how many times the right paddle has hit the ball.
        self.right_hits = right_hits

        # Tracks the current score for the left and right players.
        self.left_score = left_score
        self.right_score = right_score


class Game:
    # Sets the font used to display scores and hit counts.
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)

    # Defines some basic colours used in the game.
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # Initialises the game state, paddles, ball and scores.
    def __init__(self, window, window_width, window_height):
        # Stores window dimensions and reference to the pygame surface.
        self.window_width = window_width
        self.window_height = window_height
        self.window = window

        # Creates the left paddle near the left edge, vertically centred.
        self.left_paddle = Paddle(
            10, self.window_height // 2 - Paddle.HEIGHT // 2
        )

        # Creates the right paddle near the right edge, vertically centred.
        self.right_paddle = Paddle(
            self.window_width - 10 - Paddle.WIDTH,
            self.window_height // 2 - Paddle.HEIGHT // 2,
        )

        # Creates the ball in the middle of the window.
        self.ball = Ball(self.window_width // 2, self.window_height // 2)

        # Initialises scores and hit counters for both players.
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0

    # Draws the current score for both players onto the window.
    def _draw_score(self):
        left_score_text = self.SCORE_FONT.render(
            f"{self.left_score}", 1, self.WHITE
        )
        right_score_text = self.SCORE_FONT.render(
            f"{self.right_score}", 1, self.WHITE
        )

        # Positions the scores at the top left and top right quarter of the screen.
        self.window.blit(
            left_score_text,
            (self.window_width // 4 - left_score_text.get_width() // 2, 20),
        )
        self.window.blit(
            right_score_text,
            (self.window_width * (3 / 4) - right_score_text.get_width() // 2, 20),
        )

    # Draws the total number of hits (combined for both paddles) at the top centre.
    def _draw_hits(self):
        hits_text = self.SCORE_FONT.render(
            f"{self.left_hits + self.right_hits}", 1, self.RED
        )
        self.window.blit(
            hits_text,
            (self.window_width // 2 - hits_text.get_width() // 2, 10),
        )

    # Draws the dashed vertical divider line in the middle of the screen.
    def _draw_divider(self):
        for i in range(10, self.window_height, self.window_height // 20):
            # Skips every other segment to create the dashed effect.
            if i % 2 == 1:
                continue

            pygame.draw.rect(
                self.window,
                self.WHITE,
                (self.window_width // 2 - 5, i, 10, self.window_height // 20),
            )

    # Handles collisions between the ball, paddles, and top/bottom walls.
    def _handle_collision(self):
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        # Bounces the ball off the top and bottom edges.
        if ball.y + ball.RADIUS >= self.window_height:
            ball.y_vel *= -1
        elif ball.y - ball.RADIUS <= 0:
            ball.y_vel *= -1

        # Handles collisions when the ball is moving left.
        if ball.x_vel < 0:
            # Checks if the ball is vertically aligned with the left paddle.
            if left_paddle.y <= ball.y <= left_paddle.y + Paddle.HEIGHT:
                # Checks if the ball has reached the left paddle horizontally.
                if ball.x - ball.RADIUS <= left_paddle.x + Paddle.WIDTH:
                    ball.x_vel *= -1

                    # Calculates a new y velocity based on where the ball hit the paddle.
                    middle_y = left_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel

                    # Increments the left paddle hit counter.
                    self.left_hits += 1

        # Handles collisions when the ball is moving right.
        else:
            if right_paddle.y <= ball.y <= right_paddle.y + Paddle.HEIGHT:
                if ball.x + ball.RADIUS >= right_paddle.x:
                    ball.x_vel *= -1

                    # Calculates a new y velocity based on where the ball hit the paddle.
                    middle_y = right_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel

                    # Increments the right paddle hit counter.
                    self.right_hits += 1

    # Draws the entire frame: background, divider, scores, hits, paddles and ball.
    def draw(self, draw_score=True, draw_hits=False):
        # Fills the screen with the background colour.
        self.window.fill(self.BLACK)

        # Draws the centre divider line.
        self._draw_divider()

        # Optionally draws the score and total hits.
        if draw_score:
            self._draw_score()

        if draw_hits:
            self._draw_hits()

        # Draws both paddles.
        for paddle in [self.left_paddle, self.right_paddle]:
            paddle.draw(self.window)

        # Draws the ball.
        self.ball.draw(self.window)

    def move_paddle(self, left=True, up=True):
        # Moves the left paddle if `left` is True.
        if left:
            # Blocks movement if trying to move above the top edge.
            if up and self.left_paddle.y - Paddle.VEL < 0:
                return False

            # Blocks movement if trying to move below the bottom edge.
            if not up and self.left_paddle.y + Paddle.HEIGHT > self.window_height:
                return False

            # Applies the movement to the left paddle.
            self.left_paddle.move(up)

        # Moves the right paddle if `left` is False.
        else:
            # Blocks movement if trying to move above the top edge.
            if up and self.right_paddle.y - Paddle.VEL < 0:
                return False

            # Blocks movement if trying to move below the bottom edge.
            if not up and self.right_paddle.y + Paddle.HEIGHT > self.window_height:
                return False

            # Applies the movement to the right paddle.
            self.right_paddle.move(up)

        return True

    def loop(self):
        # Updates the ball position and processes any collisions.
        self.ball.move()
        self._handle_collision()

        # Checks if the ball went off the left or right side and updates scores.
        if self.ball.x < 0:
            self.ball.reset()
            self.right_score += 1
        elif self.ball.x > self.window_width:
            self.ball.reset()
            self.left_score += 1

        # Packages the current game state into a GameInformation object.
        game_info = GameInformation(
            self.left_hits,
            self.right_hits,
            self.left_score,
            self.right_score,
        )

        return game_info

    # Resets the ball, paddles, scores, and hit counters back to their starting values.
    def reset(self):
        # Resets the entire game.
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0