import pygame
import pickle
import neat
import os
from core.constants import TRAINED_MODEL, WIDTH, HEIGHT
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
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", TRAINED_MODEL)
    net_red = load_net(model_path, config_path)
    game.test_ai(controller_yellow='manual', controller_red='ai', net_red=net_red, draw=True)

def play_ai_vs_human():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    game = SpaceGame(win)
    config_path = "scripts/config.txt"
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", TRAINED_MODEL)
    net_yellow = load_net(model_path, config_path)
    game.test_ai(controller_yellow='ai', net_yellow=net_yellow, controller_red='manual', draw=True)

def play_ai_vs_ai():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    game = SpaceGame(win)
    config_path = "scripts/config.txt"
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", TRAINED_MODEL)
    net_yellow = load_net(model_path, config_path)
    net_red = load_net(model_path, config_path)
    game.test_ai(controller_yellow='ai', net_yellow=net_yellow,
                 controller_red='ai', net_red=net_red, draw=True)

def play_random_vs_ai():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    game = SpaceGame(win)
    config_path = "scripts/config.txt"
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", TRAINED_MODEL)
    net_red = load_net(model_path, config_path)
    game.test_ai(controller_yellow='random', controller_red='ai', net_red=net_red, draw=True)

if __name__ == "__main__":
    print("Choose a mode to run:")
    print("1 - Human vs Human")
    print("2 - Human vs AI")
    print("3 - AI vs Human")
    print("4 - AI vs AI")
    print("5 - Random vs AI")
    
    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        play_human_vs_human()
    elif choice == "2":
        play_human_vs_ai()
    elif choice == "3":
        play_ai_vs_human()
    elif choice == "4":
        play_ai_vs_ai()
    elif choice == "5":
        play_random_vs_ai()
    else:
        print("Invalid choice. Please run the program again.")

