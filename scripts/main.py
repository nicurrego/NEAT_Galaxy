import os
import pickle
import random
import neat
import pygame

from core.game import Game
from core.actions import Action
from core.constants import WIDTH, HEIGHT, FPS

MAX_BULLETS = 3  # Must match your core constants

class SpaceGame:
    def __init__(self, window):
        self.game = Game(window)
        self.yellow_ship = self.game.yellow_ship
        self.red_ship = self.game.red_ship

    def calculate_fitness(self, hits, lives_left, steps_survived, win, movement=0):
        """
        Calculate fitness based on various metrics.
        - hits: Number of hits scored
        - lives_left: How many lives left at end
        - steps_survived: Number of steps survived
        - win: True if this agent won
        - movement: Optional, number of moves made (not used unless you count moves)
        """
        HIT_REWARD = 10        
        SURVIVAL_REWARD = 1    
        STEP_REWARD = 0.02
        WIN_BONUS = 15
        MOVEMENT_REWARD = 0.01 

        fitness = (
            hits * HIT_REWARD +
            lives_left * SURVIVAL_REWARD +
            steps_survived * STEP_REWARD +
            (WIN_BONUS if win else 0) +
            movement * MOVEMENT_REWARD
        )
        return fitness

    def train_ai(self, genome1, genome2, config, draw=False, max_steps=2000):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        clock = pygame.time.Clock()
        done = False
        step_count = 0

        yellow_moves = 0
        red_moves = 0

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True  # Force quit

            obs1 = self.observe(self.yellow_ship, self.red_ship)
            obs2 = self.observe(self.red_ship, self.yellow_ship)

            output1 = net1.activate(obs1)
            output2 = net2.activate(obs2)

            action1 = self.output_to_action(output1)
            action2 = self.output_to_action(output2)

            # Track only true movement (not STAY or SHOOT)
            if action1 in [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]:
                yellow_moves += 1
            if action2 in [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]:
                red_moves += 1


            self.game.move_spaceship(self.yellow_ship, action1)
            self.game.move_spaceship(self.red_ship, action2)

            self.game.update()

            if draw:
                self.game.draw()

            step_count += 1
            if self.game.is_game_over() or step_count >= max_steps:
                done = True

            # When draw=False, run as fast as possible
            if draw:
                clock.tick(FPS)

        # Fitness metrics
        y_hits = self.game.yellow_hits
        r_hits = self.game.red_hits
        y_lives = self.game.yellow_lives
        r_lives = self.game.red_lives
        yellow_win = r_lives <= 0
        red_win = y_lives <= 0

        # Assign fitness using your new method!
        genome1.fitness = self.calculate_fitness(y_hits, y_lives, step_count, yellow_win, yellow_moves)
        genome2.fitness = self.calculate_fitness(r_hits, r_lives, step_count, red_win, red_moves)
        return False

    # --- test_ai stays unchanged for human/AI testing in scripts/play_match.py ---
    def test_ai(
        self,
        net_yellow=None,
        net_red=None,
        config=None,
        controller_yellow='manual',
        controller_red='manual',
        draw=True,
        max_steps=1000,
    ):
        clock = pygame.time.Clock()
        step_count = 0
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

            # Yellow Ship Control
            if controller_yellow == 'manual':
                keys = pygame.key.get_pressed()
                action_yellow = Action.STAY
                if keys[pygame.K_w]:
                    action_yellow = Action.UP
                elif keys[pygame.K_s]:
                    action_yellow = Action.DOWN
                elif keys[pygame.K_a]:
                    action_yellow = Action.LEFT
                elif keys[pygame.K_d]:
                    action_yellow = Action.RIGHT
                elif keys[pygame.K_f]:
                    action_yellow = Action.SHOOT
            elif controller_yellow == 'ai' and net_yellow is not None:
                obs = self.observe(self.yellow_ship, self.red_ship)
                output = net_yellow.activate(obs)
                action_yellow = self.output_to_action(output)
            elif controller_yellow == 'random':
                action_yellow = Action(random.randint(0, 5))
            else:
                action_yellow = Action.STAY

            # Red Ship Control
            if controller_red == 'manual':
                keys = pygame.key.get_pressed()
                action_red = Action.STAY
                if keys[pygame.K_UP]:
                    action_red = Action.UP
                elif keys[pygame.K_DOWN]:
                    action_red = Action.DOWN
                elif keys[pygame.K_LEFT]:
                    action_red = Action.LEFT
                elif keys[pygame.K_RIGHT]:
                    action_red = Action.RIGHT
                elif keys[pygame.K_SLASH]:
                    action_red = Action.SHOOT
            elif controller_red == 'ai' and net_red is not None:
                obs = self.observe(self.red_ship, self.yellow_ship)
                output = net_red.activate(obs)
                action_red = self.output_to_action(output)
            elif controller_red == 'random':
                action_red = Action(random.randint(0, 5))
            else:
                action_red = Action.STAY

            self.game.move_spaceship(self.yellow_ship, action_yellow)
            self.game.move_spaceship(self.red_ship, action_red)
            self.game.update()

            if draw:
                self.game.draw()

            step_count += 1
            if self.game.is_game_over() or step_count >= max_steps:
                done = True

            clock.tick(FPS)
        return False

    def observe(self, ship, enemy):
        obs = []
        # Spaceship positions
        obs.append(ship.x)
        obs.append(ship.y)
        obs.append(enemy.x)
        obs.append(enemy.y)
        # Own bullets
        for i in range(MAX_BULLETS):
            if i < len(ship.bullets):
                obs.append(ship.bullets[i].x)
                obs.append(ship.bullets[i].y)
            else:
                obs.append(-1)
                obs.append(-1)
        # Enemy bullets
        for i in range(MAX_BULLETS):
            if i < len(enemy.bullets):
                obs.append(enemy.bullets[i].x)
                obs.append(enemy.bullets[i].y)
            else:
                obs.append(-1)
                obs.append(-1)
        # Optionally: add more info
        # obs.append(self.game.yellow_lives)
        # obs.append(self.game.red_lives)
        return obs

    def output_to_action(self, output):
        return Action(output.index(max(output)))

def eval_genomes(genomes, config):
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Galaxy NEAT")

    for i, (genome_id1, genome1) in enumerate(genomes):
        print(round(i/len(genomes) * 100), end=" ")
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i+1, len(genomes) - 1):]:
            if genome2.fitness is None:
                genome2.fitness = 0
            galaxy = SpaceGame(win)
            # ---- Training mode: draw=False, max_steps=2000 ----
            force_quit = galaxy.train_ai(genome1, genome2, config, draw=False, max_steps=2000)
            if force_quit:
                quit()

def run_neat(config_path):
    config = neat.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path
    )
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-29')
    # p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 1)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    pygame.init()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run_neat(config_path)
