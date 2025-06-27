import pygame
from enum import Enum

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Screen dimensions
WIDTH = 720
HEIGHT = 360

# Spaceships area
MIDLE_WIDTH = 10
MIDLE_LEFT = WIDTH // 2 - MIDLE_WIDTH
MIDLE_HEIGHT = HEIGHT

# Spaceship
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40

# Game properties
FPS = 60
VEL = 5
BORDER_WIDTH = 10
SHOOTING_DELAY_MS = 100
MAX_BULLETS = 3


class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    STAY = 4
    SHOOT = 5

    @classmethod
    def all(cls):
        return list(cls)
    
class Bullet:
    """Represents a bullet fired by a spaceship."""
    def __init__(self, x, y, direction, color, speed=10):
        """
        Initialize a bullet.
        x, y: Position
        direction: +1 (right), -1 (left)
        color: Bullet color
        speed: Bullet speed
        """
        self.x = x
        self.y = y
        self.direction = direction  # +1 for right, -1 for left
        self.color = color
        self.speed = speed
        self.width = 10
        self.height = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        """Move the bullet in its direction."""
        self.x += self.speed * self.direction
        self.rect.x = self.x

    def draw(self, surface):
        """Draw the bullet on the given surface."""
        pygame.draw.rect(surface, self.color, self.rect)

    def is_off_screen(self):
        """Check if the bullet is outside the screen."""
        return self.x < 0 or self.x > WIDTH

    def collides_with(self, other_rect):
        """Check collision with another rect."""
        return self.rect.colliderect(other_rect)
    

class Spaceship:
    """Represents a spaceship that can move and shoot."""
    def __init__(self, x, y, image, bullet_color=WHITE, direction=1):
        """
        Initialize a spaceship.
        x, y: Position
        image: Pygame surface for the ship
        bullet_color: Color of bullets
        direction: +1 (right), -1 (left)
        """
        self.x = x
        self.y = y
        self.image = image
        self.bullets = []
        self.bullet_color = bullet_color
        self.direction = direction # 1 for right, -1 for left
        self.rect = pygame.Rect(self.x, self.y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.last_shot_tick = 0
        self.shoot_delay_ms = SHOOTING_DELAY_MS

    def move(self, dx, dy):
        """Move the spaceship, staying within bounds and not crossing the middle."""
        new_x = min(max(self.x + dx, 0), WIDTH - SPACESHIP_WIDTH)
        new_y = min(max(self.y + dy, 0), HEIGHT - SPACESHIP_HEIGHT)
        new_rect = pygame.Rect(new_x, new_y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        middle_rect = pygame.Rect(MIDLE_LEFT, 0, MIDLE_WIDTH, MIDLE_HEIGHT)
        # Prevent crossing the middle barrier
        if not new_rect.colliderect(middle_rect):
            self.x = new_x
        self.y = new_y
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        """Draw the spaceship and its bullets."""
        if self.image:
            surface.blit(self.image, (self.x, self.y))
        else:
            if self.bullet_color == RED:
                pygame.draw.rect(surface, (RED), (self.x, self.y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
            else:
                pygame.draw.rect(surface, (YELLOW), (self.x, self.y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
        # Draw all bullets
        for bullet in self.bullets:
            bullet.draw(surface)

    def shoot(self):
        """Fire a bullet if shooting delay allows."""
        now = pygame.time.get_ticks()
        if now - self.last_shot_tick < self.shoot_delay_ms:
            return
        self.last_shot_tick = now
        # Bullet starts at front of ship
        if self.direction == 1:
            bullet_x = self.x + SPACESHIP_WIDTH
        else:
            bullet_x = self.x
        bullet_y = self.y + SPACESHIP_HEIGHT//2 - 2

        # Limit max numer of bullets
        if len(self.bullets) < MAX_BULLETS:
            new_bullet = Bullet(bullet_x, bullet_y, self.direction, self.bullet_color)
            self.bullets.append(new_bullet)

    def update_bullets(self):
        """Update all bullets, removing those off-screen."""
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)