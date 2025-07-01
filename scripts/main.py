import os
import pickle
import neat
import pygame
from core.game import Game
from core.actions import Action



class SpaceGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.yellow_ship = self.game.yellow_ship
        self.red_ship = self.game.red_ship

# def train_ai(self, genome1, )

def eval_genomes(genomes, config):
    width, height = 720, 360
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Galaxy NEAT")

    for i, (genome_id1, genome1) in enumerate(genomes):
        print(round(i/len(genomes)* 100), end=" ")
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i+1, len(genomes) - 1):]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            galaxy = SpaceGame(win, width, height)

            force_quit = galaxy.train_ai(genome1, genome2, config, draw=True)
            if force_quit:
                quit()

def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-85')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')


    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)