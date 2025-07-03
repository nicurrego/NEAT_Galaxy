class FitnessCalculator:
    def __init__(self, config=None):
        """
        Initialize with optional config dictionary to override defaults
        """
        # Default values
        self.hit_reward = 0
        self.survival_reward = 0
        self.step_reward = 0
        self.win_bonus = 0
        self.movement_reward = 0
        
        # Override with config if provided
        if config:
            for key, value in config.items():
                if hasattr(self, key):
                    setattr(self, key, value)
    
    def calculate(self, hits, lives_left, steps_survived, win, movement=0):
        """
        Calculate fitness based on various metrics.
        """

        fitness = (
            hits * self.hit_reward +
            lives_left * self.survival_reward +
            steps_survived * self.step_reward +
            (self.win_bonus if win else 0) +
            movement * self.movement_reward
        )
        return fitness