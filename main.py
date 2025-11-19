import pygame
from pong import Game
import neat
import os
import pickle


class PongGame:
    # Handles the setup and logic for AI-controlled Pong games.
    def __init__(self, window, width, height):
        # Creates the Pong game instance.
        self.game = Game(window, width, height)

        # Stores references to the paddles and ball.
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball

    # Runs a single-player test where the left paddle is human-controlled
    # and the right paddle is controlled by the trained NEAT AI.
    def test_ai(self, genome, config):
        # Builds a neural network from the genome and NEAT configuration.
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        # Keeps track of whether the game loop should continue running.
        run = True

        # Limits the game to 60 FPS.
        clock = pygame.time.Clock()

        while run:
            # Keeps the game running at a stable frame rate.
            clock.tick(60)

            # Handles window events like closing the game.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            # Checks for player input to move the left paddle.
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)
            if keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)

            # Passes the right paddle’s y position, the ball’s y position, and horizontal distance between them into the neural network.
            output = net.activate(
                (self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x))
            )

            # Determines which action to take based on the network’s output.
            decision = output.index(max(output))

            # 0 = stay still, 1 = move up, 2 = move down.
            if decision == 0:
                pass
            elif decision == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            # Updates the game state and draws the new frame.
            game_info = self.game.loop()
            self.game.draw(draw_score=True, draw_hits=False)
            pygame.display.update()

        # Shuts down pygame once the test ends.
        pygame.quit()

    # Runs training matches between two AI agents using their genomes.
    def train_ai(self, genome1, genome2, config):
        # Builds neural networks for both genomes.
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        # Keeps the match running until a stop condition is met.
        run = True

        while run:
            # Handles quit events so the window can be closed safely.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # Activates the first network to control the left paddle.
            output1 = net1.activate(
                (self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x))
            )
            decision1 = output1.index(max(output1))

            # 0 = do nothing, 1 = move up, 2 = move down.
            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.move_paddle(left=True, up=True)
            else:
                self.game.move_paddle(left=True, up=False)

            # Activates the second network to control the right paddle.
            output2 = net2.activate(
                (self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x))
            )
            decision2 = output2.index(max(output2))

            # 0 = do nothing, 1 = move up, 2 = move down.
            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            # Updates game state and redraws the frame.
            game_info = self.game.loop()
            self.game.draw(draw_score=False, draw_hits=True)
            pygame.display.update()

            # Ends the match if a player scores or goes on too long.
            if (
                game_info.left_score >= 1
                or game_info.right_score >= 1
                or game_info.left_hits > 50
            ):
                # Updates the fitness scores for both genomes based on how well they played.
                self.calculate_fitness(genome1, genome2, game_info)
                break

    # Updates the fitness score for both genomes based on paddle-ball hits.
    def calculate_fitness(self, genome1, genome2, game_info):
        genome1.fitness += game_info.left_hits
        genome2.fitness += game_info.right_hits


# Evaluates all genomes in the NEAT population by having them play against each other.
def eval_genomes(genomes, config):
    # Sets up the game window.
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))

    # Loops through each genome and pairs it against others.
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break

        genome1.fitness = 0

        # Plays matches between genome1 and every other genome that comes after it.
        for genome_id2, genome2 in genomes[i + 1:]:
            if genome2.fitness is None:
                genome2.fitness = 0

            game = PongGame(window, width, height)
            game.train_ai(genome1, genome2, config)


# Runs the NEAT training algorithm to evolve better performing AIs.
def run_neat(config):
    # Starts a fresh NEAT population using the given configuration.
    p = neat.Population(config)

    # Adds console output and statistics tracking.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Saves a checkpoint every generation.
    p.add_reporter(neat.Checkpointer(1))

    # Evolves the population; second argument is number of generations.
    winner = p.run(eval_genomes, 1)

    # Saves the best genome so it can be loaded and tested later.
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


# Tests the trained AI by running it against a human or as a demo.
def test_ai(config):
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))

    # Loads the best saved genome from file.
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    # Creates a PongGame instance and runs the test with the trained AI.
    game = PongGame(window, width, height)
    game.test_ai(winner, config)


if __name__ == "__main__":
    # Finds the NEAT configuration file in the current directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    # Builds the NEAT configuration object.
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    # Uncomment one of these depending on whether you want to train or test:
    # run_neat(config)
    test_ai(config)