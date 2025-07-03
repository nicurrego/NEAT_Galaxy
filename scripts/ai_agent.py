from core.actions import Action

class AIAgent:
    def __init__(self, game, max_bullets=3):
        self.game = game
        self.max_bullets = max_bullets
        
    def observe(self, ship, enemy):
        """
        Create observation vector for the neural network
        """
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
        for i in range(self.max_bullets):
            if i < len(ship.bullets):
                obs.append(ship.bullets[i].x)
                obs.append(ship.bullets[i].y)
            else:
                obs.append(-1)
                obs.append(-1)
                
        # Enemy bullets
        for i in range(self.max_bullets):
            if i < len(enemy.bullets):
                obs.append(enemy.bullets[i].x)
                obs.append(enemy.bullets[i].y)
            else:
                obs.append(-1)
                obs.append(-1)
                
        # Add lives information
        obs.append(self.game.yellow_lives if ship == self.game.yellow_ship else self.game.red_lives)
        obs.append(self.game.red_lives if ship == self.game.yellow_ship else self.game.yellow_lives)
        
        return obs
    
    def output_to_action(self, output):
        """
        Convert neural network output to game action
        """
        return Action(output.index(max(output)))