import os
import pickle
import neat
import pygame
from core.constants import WIDTH, HEIGHT

class NEATTrainer:
    def __init__(self, game_class, config_path, models_dir):
        self.game_class = game_class
        self.config_path = config_path
        self.models_dir = models_dir
        self.config = neat.Config(
            neat.DefaultGenome, neat.DefaultReproduction,
            neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path
        )
        
    def eval_genomes(self, genomes, config, visualize=False, visualize_top=5, draw_training=False):
        """
        Evaluate genomes with options for visualization.
        
        Parameters:
        - visualize: Whether to visualize top genomes after evaluation
        - visualize_top: Number of top genomes to visualize (if visualize=True)
        - draw_training: Whether to draw all games during training (slows down training)
        """
        win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Galaxy NEAT")

        # First pass: evaluate all genomes with optional drawing
        for i, (genome_id1, genome1) in enumerate(genomes):
            print(f"Evaluating genome {i+1}/{len(genomes)}: {genome_id1}", end="\r")
            genome1.fitness = 0
            for genome_id2, genome2 in genomes[min(i+1, len(genomes) - 1):]:
                if genome2.fitness is None:
                    genome2.fitness = 0
                game = self.game_class(win)
                force_quit = game.train_ai(genome1, genome2, config, draw=draw_training, max_steps=2000)
                if force_quit:
                    quit()
    
        # If visualization is requested, show top genomes
        if visualize and visualize_top > 0:
            # Sort genomes by fitness
            sorted_genomes = sorted(genomes, key=lambda x: x[1].fitness, reverse=True)
            top_genomes = sorted_genomes[:min(visualize_top, len(sorted_genomes))]
            
            print("\nVisualizing top performing genomes:")
            for i, (genome_id1, genome1) in enumerate(top_genomes):
                if i+1 < len(top_genomes):
                    genome_id2, genome2 = top_genomes[i+1]
                    print(f"Visualizing match between genome {genome_id1} (fitness: {genome1.fitness:.2f}) and {genome_id2} (fitness: {genome2.fitness:.2f})")
                    game = self.game_class(win)
                    game.train_ai(genome1, genome2, config, draw=True, max_steps=1000)
                    pygame.time.delay(500)  # Brief pause between visualizations
    
    def run(self, generations=50, restore_checkpoint=None, visualize=False, visualize_top=5, draw_training=False):
        """
        Run the NEAT algorithm to train the neural network.
        
        Parameters:
        - generations: Number of generations to run
        - restore_checkpoint: Checkpoint number to restore from (if any)
        - visualize: Whether to visualize top genomes after evaluation
        - visualize_top: Number of top genomes to visualize
        - draw_training: Whether to draw all games during training (slows down training)
        """
        # Create the population
        if restore_checkpoint:
            checkpoint_path = os.path.join(self.models_dir, f"neat-checkpoint-{restore_checkpoint}")
            p = neat.Checkpointer.restore_checkpoint(checkpoint_path)
        else:
            p = neat.Population(self.config)
            
        # Add reporters
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        
        # Save checkpoints
        checkpoint_prefix = os.path.join(self.models_dir, "neat-checkpoint-")
        p.add_reporter(neat.Checkpointer(2, filename_prefix=checkpoint_prefix))

        # Create a custom eval_genomes function that includes visualization parameters
        def eval_genomes_wrapper(genomes, config):
            return self.eval_genomes(genomes, config, visualize=visualize, 
                                    visualize_top=visualize_top, draw_training=draw_training)

        # Run for up to n generations
        winner = p.run(eval_genomes_wrapper, generations)
        
        # Save the winner
        best_path = os.path.join(self.models_dir, "best.pickle")
        with open(best_path, "wb") as f:
            pickle.dump(winner, f)
            
        return winner




