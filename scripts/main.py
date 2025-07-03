import os
import pickle
import neat
import pygame

from core.game import Game
from core.actions import Action
from core.constants import CHECKPOINT, HIT_REWARD, MOVEMENT_REWARD, STEP_REWARD, SURVIVAL_REWARD, WIDTH, HEIGHT, FPS, WIN_BONUS
from scripts.neat_trainer import NEATTrainer
from scripts.fitness_calculator import FitnessCalculator
from scripts.ai_agent import AIAgent

MAX_BULLETS = 3

class SpaceGame:
    def __init__(self, window):
        self.game = Game(window)
        self.yellow_ship = self.game.yellow_ship
        self.red_ship = self.game.red_ship
        self.agent = AIAgent(self.game, MAX_BULLETS)
        
        # Initialize fitness calculator with default values
        # These can be adjusted for different experiments
        fitness_config = {
            "hit_reward": HIT_REWARD,
            "survival_reward": SURVIVAL_REWARD,
            "step_reward": STEP_REWARD,
            "win_bonus": WIN_BONUS,
            "movement_reward": MOVEMENT_REWARD
        }
        self.fitness_calculator = FitnessCalculator(fitness_config)

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

            obs1 = self.agent.observe(self.yellow_ship, self.red_ship)
            obs2 = self.agent.observe(self.red_ship, self.yellow_ship)

            output1 = net1.activate(obs1)
            output2 = net2.activate(obs2)

            action1 = self.agent.output_to_action(output1)
            action2 = self.agent.output_to_action(output2)

            # Track movement
            if action1.value < 4:  # UP, DOWN, LEFT, RIGHT
                yellow_moves += 1
            if action2.value < 4:
                red_moves += 1

            self.game.move_spaceship(self.yellow_ship, action1)
            self.game.move_spaceship(self.red_ship, action2)

            self.game.update()

            if draw:
                self.game.draw(draw_score=True, draw_hits=True)

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

        # Use the fitness calculator to calculate fitness
        genome1.fitness = self.fitness_calculator.calculate(
            y_hits, y_lives, step_count, yellow_win, yellow_moves
        )
        genome2.fitness = self.fitness_calculator.calculate(
            r_hits, r_lives, step_count, red_win, red_moves
        )
        return False

    def test_ai(self, controller_yellow='manual', controller_red='manual', 
                net_yellow=None, net_red=None, draw=True):
        """
        Test AI agents against each other or human players.
        
        Parameters:
        - controller_yellow/red: 'manual', 'ai', or 'random'
        - net_yellow/red: Neural networks for AI controllers
        """
        clock = pygame.time.Clock()
        self.game.reset()
        
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            # Get actions based on controller type
            action_yellow = self._get_action(controller_yellow, self.yellow_ship, self.red_ship, net_yellow)
            action_red = self._get_action(controller_red, self.red_ship, self.yellow_ship, net_red)
            
            # Apply actions
            self.game.move_spaceship(self.yellow_ship, action_yellow)
            self.game.move_spaceship(self.red_ship, action_red)
            
            # Update game state
            self.game.update()
            
            # Check for game over
            if self.game.is_game_over():
                running = False
            
            # Small delay to make the game playable
            pygame.time.delay(10)
            
        self.game.draw()
        pygame.display.update()
        pygame.time.delay(2000)
        
    def _get_action(self, controller_type, ship, enemy_ship, net=None):
        """Helper method to get actions based on controller type"""
        if controller_type == 'manual':
            return self._get_manual_action(ship)
        elif controller_type == 'ai' and net is not None:
            obs = self.agent.observe(ship, enemy_ship)
            output = net.activate(obs)
            return self.agent.output_to_action(output)
        elif controller_type == 'random':
            import random
            from core.actions import Action
            return random.choice(list(Action))
        else:
            # Default to STAY if invalid controller
            return Action.STAY
        
    def _get_manual_action(self, ship):
        """Get manual action from keyboard input"""
        from core.actions import Action
        keys = pygame.key.get_pressed()
        
        # Yellow ship controls (WASD + SPACE)
        if ship == self.yellow_ship:
            if keys[pygame.K_w]:
                return Action.UP
            if keys[pygame.K_s]:
                return Action.DOWN
            if keys[pygame.K_a]:
                return Action.LEFT
            if keys[pygame.K_d]:
                return Action.RIGHT
            if keys[pygame.K_SPACE]:
                return Action.SHOOT
        # Red ship controls (Arrow keys + RCTRL)
        else:
            if keys[pygame.K_UP]:
                return Action.UP
            if keys[pygame.K_DOWN]:
                return Action.DOWN
            if keys[pygame.K_LEFT]:
                return Action.LEFT
            if keys[pygame.K_RIGHT]:
                return Action.RIGHT
            if keys[pygame.K_RCTRL]:
                return Action.SHOOT
            
        return Action.STAY

    def observe(self, ship, enemy):
        obs = []
        # Spaceship positions
        obs.append(ship.x)
        obs.append(ship.y)
        obs.append(enemy.x)
        obs.append(enemy.y)
        
        # Distance to enemy (helps with targeting)
        dx = enemy.x - ship.x
        dy = enemy.y - ship.y
        obs.append(dx)
        obs.append(dy)
        
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
            
        # Add lives information
        obs.append(self.game.yellow_lives if ship == self.yellow_ship else self.game.red_lives)
        obs.append(self.game.red_lives if ship == self.yellow_ship else self.game.yellow_lives)
        
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

            force_quit = galaxy.train_ai(genome1, genome2, config, draw=True, max_steps=2000)
            if force_quit:
                quit()

def run_neat(config_path, models_dir):
    config = neat.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path
    )
    # Save checkpoints in .models/
    checkpoint_prefix = os.path.join(models_dir, CHECKPOINT)
    # p = neat.Checkpointer.restore_checkpoint(".neat-checkpoint-31")
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(2, filename_prefix=checkpoint_prefix))

    winner = p.run(eval_genomes, 1) 
    best_path = os.path.join(models_dir, "best.pickle")
    with open(best_path, "wb") as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    pygame.init()
    local_dir = os.path.dirname(__file__)
    models_dir = os.path.join(local_dir, "..", "models")
    os.makedirs(models_dir, exist_ok=True)

    config_path = os.path.join(local_dir, "config.txt")
    
    # Create and run the trainer with visualization options
    trainer = NEATTrainer(SpaceGame, config_path, models_dir)
    
    # Set visualize=True to see top genomes in action
    trainer.run(generations=50, visualize=True, visualize_top=3)

