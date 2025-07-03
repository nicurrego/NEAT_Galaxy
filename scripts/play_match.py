import pygame
import pickle
import neat
import os
from core.constants import WIDTH, HEIGHT, FPS
from scripts.main import SpaceGame

def load_net(pickle_path, config_path):
    with open(pickle_path, "rb") as f:
        genome = pickle.load(f)
    config = neat.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path
    )
    return neat.nn.FeedForwardNetwork.create(genome, config)

def play_human_vs_human():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    game = SpaceGame(win)
    game.test_ai(controller_yellow='manual', controller_red='manual', draw=True)

def play_human_vs_ai():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    game = SpaceGame(win)
    config_path = "scripts/config.txt"
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", "best.pickle")
    net_red = load_net(model_path, config_path)
    game.test_ai(controller_yellow='manual', controller_red='ai', net_red=net_red, draw=True)

def play_ai_vs_human():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    game = SpaceGame(win)
    config_path = "scripts/config.txt"
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", "best.pickle")
    net_yellow = load_net(model_path, config_path)
    game.test_ai(controller_yellow='ai', net_yellow=net_yellow, controller_red='manual', draw=True)

def play_ai_vs_ai():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    game = SpaceGame(win)
    config_path = "scripts/config.txt"
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", "best.pickle")
    net_yellow = load_net(model_path, config_path)
    net_red = load_net(model_path, config_path)
    game.test_ai(controller_yellow='ai', net_yellow=net_yellow,
                 controller_red='ai', net_red=net_red, draw=True)

def play_random_vs_ai():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    game = SpaceGame(win)
    config_path = "scripts/config.txt"
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", "best.pickle")
    net_red = load_net(model_path, config_path)
    game.test_ai(controller_yellow='random', controller_red='ai', net_red=net_red, draw=True)

if __name__ == "__main__":
    # Uncomment the experiments you want to run:
    
    # play_human_vs_human()
    # play_human_vs_ai()
    # play_ai_vs_human()
    play_ai_vs_ai()
    # play_random_vs_ai()
