import pygame

from core.constants import WIDTH


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
 