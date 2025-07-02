import random
import pygame
from core.constants import (
    MIDLE_LEFT, MIDLE_WIDTH, WIDTH, HEIGHT, BLACK, WHITE, RED, YELLOW,
    FPS
)
from core.spaceship import Spaceship
from core.actions import Action

class GameInformation:
    def __init__(self, yellow_hits, red_hits, yellow_lives, red_lives):
        self.yellow_hits = yellow_hits
        self.red_hits = red_hits
        self.yellow_lives = yellow_lives
        self.red_lives = red_lives

class Game:
    def __init__(self, window, yellow_image=None, red_image=None):
        self.SCORE_FONT = pygame.font.SysFont("comicsans", 16)
        self.window = window

        # Init ships
        self.yellow_ship = Spaceship(
            x=50, y=HEIGHT // 2 - 20, image=yellow_image, bullet_color=YELLOW, direction=1
        )
        self.red_ship = Spaceship(
            x=WIDTH - 50 - 55, y=HEIGHT // 2 - 20, image=red_image, bullet_color=RED, direction=-1
        )

        # Scores / hits / lives
        self.yellow_lives = 3
        self.red_lives = 3
        self.yellow_hits = 0
        self.red_hits = 0

    def _draw_divider(self):
        # pygame.draw.rect(
        #     self.window,
        #     WHITE,
        #     (MIDLE_LEFT, 0, MIDLE_WIDTH, HEIGHT)
        # )
        pass

    def _draw_score(self):
        yellow_text = self.SCORE_FONT.render(
            f"Yellow Lives: {self.yellow_lives}", True, YELLOW
        )
        red_text = self.SCORE_FONT.render(
            f"Red Lives: {self.red_lives}", True, RED
        )
        self.window.blit(yellow_text, (20, 10))
        self.window.blit(red_text, (WIDTH - red_text.get_width() - 20, 10))

    def _draw_hits(self):
        hits_text = self.SCORE_FONT.render(
            f"Y Hits: {self.yellow_hits}  |  R Hits: {self.red_hits}", True, WHITE
        )
        self.window.blit(hits_text, (WIDTH//2 - hits_text.get_width()//2, 40))

    def handle_events(self, keys_pressed):
        """Move ships based on input dictionary {ship: (dx, dy)}."""
        # This is a placeholder. You'll likely want to call ship.move(dx, dy) from outside
        pass

    def move_spaceship(self, ship, action):
        if action == Action.UP:
            ship.move(0, -5)
        elif action == Action.DOWN:
            ship.move(0, 5)
        elif action == Action.LEFT:
            ship.move(-5, 0)
        elif action == Action.RIGHT:
            ship.move(5, 0)
        elif action == Action.SHOOT:
            ship.shoot()
        # Action.STAY does nothing

    def check_bullet_hits(self):
        # Yellow bullets hit red?
        for bullet in self.yellow_ship.bullets[:]:
            if bullet.collides_with(self.red_ship.rect):
                self.yellow_ship.bullets.remove(bullet)
                self.yellow_hits += 1
                self.red_lives -= 1

        # Red bullets hit yellow?
        for bullet in self.red_ship.bullets[:]:
            if bullet.collides_with(self.yellow_ship.rect):
                self.red_ship.bullets.remove(bullet)
                self.red_hits += 1
                self.yellow_lives -= 1

    def update(self):
        """Call this each frame: updates bullets and handles collisions."""
        self.yellow_ship.update_bullets()
        self.red_ship.update_bullets()
        self.check_bullet_hits()

    def draw(self, draw_score=True, draw_hits=True):
        self.window.fill(BLACK)
        self._draw_divider()
        if draw_score:
            self._draw_score()
        if draw_hits:
            self._draw_hits()
        self.yellow_ship.draw(self.window)
        self.red_ship.draw(self.window)
        pygame.display.update()

    def is_game_over(self):
        return self.yellow_lives <= 0 or self.red_lives <= 0

    def reset(self):
        self.yellow_ship.x, self.yellow_ship.y = 50, HEIGHT // 2 - 20
        self.red_ship.x, self.red_ship.y = WIDTH - 50 - 55, HEIGHT // 2 - 20
        self.yellow_ship.bullets.clear()
        self.red_ship.bullets.clear()
        self.yellow_lives = 3
        self.red_lives = 3
        self.yellow_hits = 0
        self.red_hits = 0

    def get_game_info(self):
        return GameInformation(
            self.yellow_hits, self.red_hits, self.yellow_lives, self.red_lives
        )
    
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

            # --- Yellow Ship Control
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

            # --- Red Ship Control
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

