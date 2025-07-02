import pygame
import pickle
import neat
import sys
from core.constants import WIDTH, HEIGHT, FPS
from scripts.main import SpaceGame

# ---- Helper function to load a NEAT net ----
def load_net(pickle_path, config_path):
    with open(pickle_path, "rb") as f:
        genome = pickle.load(f)
    config = neat.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path
    )
    return neat.nn.FeedForwardNetwork.create(genome, config)

# ---- Main match launcher ----
if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Galaxy Arena: Play Match")

    game = SpaceGame(win)
    config_path = "scripts/config.txt"  # Adjust if needed

    # ---- Load neural nets as needed ----
    net_yellow, net_red = None, None

    # Uncomment to load an AI (adjust paths as needed)
    # net_yellow = load_net("best.pickle", config_path)
    # net_red = load_net("best.pickle", config_path)

    # ---- CHOOSE YOUR MATCHUP HERE ----
    # Examples:
    # 1. Human (yellow) vs Human (red):
    # game.test_ai(controller_yellow='manual', controller_red='manual', draw=True)

    # 2. Human (yellow, WASD+F) vs AI (red):
    # net_red = load_net("best.pickle", config_path)
    # game.test_ai(controller_yellow='manual', controller_red='ai', net_red=net_red, draw=True)

    # 3. AI (yellow) vs Human (red):
    net_yellow = load_net("best.pickle", config_path)
    game.test_ai(controller_yellow='ai', net_yellow=net_yellow, controller_red='manual', draw=True)

    # 4. AI vs AI:
    # net_yellow = load_net("best.pickle", config_path)
    # net_red = load_net("best.pickle", config_path)
    # game.test_ai(controller_yellow='ai', net_yellow=net_yellow, controller_red='ai', net_red=net_red, draw=True)

    # 5. Random vs AI:
    # net_red = load_net("best.pickle", config_path)
    # game.test_ai(controller_yellow='random', controller_red='ai', net_red=net_red, draw=True)

    # ---- UNCOMMENT ONE LINE BELOW TO CHOOSE ----

    # 1. Human vs Human
    # game.test_ai(controller_yellow='manual', controller_red='manual', draw=True)

    # 2. Human vs AI (red)
    # net_red = load_net("best.pickle", config_path)
    # game.test_ai(controller_yellow='manual', controller_red='ai', net_red=net_red, draw=True)

    # 3. AI (yellow) vs Human (red)
    # net_yellow = load_net("best.pickle", config
