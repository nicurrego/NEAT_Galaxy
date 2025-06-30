import pygame
from core.game import Game
from core.actions import Action

pygame.init()
window = pygame.display.set_mode((720, 360))
pygame.display.set_caption("Spaceship Battle")

game = Game(window)

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # Control yellow (WASD + F to shoot)
    if keys[pygame.K_w]:
        game.move_spaceship(game.yellow_ship, Action.UP)
    if keys[pygame.K_s]:
        game.move_spaceship(game.yellow_ship, Action.DOWN)
    if keys[pygame.K_a]:
        game.move_spaceship(game.yellow_ship, Action.LEFT)
    if keys[pygame.K_d]:
        game.move_spaceship(game.yellow_ship, Action.RIGHT)
    if keys[pygame.K_f]:
        game.move_spaceship(game.yellow_ship, Action.SHOOT)
    # Control red (Arrows + slash to shoot)
    if keys[pygame.K_UP]:
        game.move_spaceship(game.red_ship, Action.UP)
    if keys[pygame.K_DOWN]:
        game.move_spaceship(game.red_ship, Action.DOWN)
    if keys[pygame.K_LEFT]:
        game.move_spaceship(game.red_ship, Action.LEFT)
    if keys[pygame.K_RIGHT]:
        game.move_spaceship(game.red_ship, Action.RIGHT)
    if keys[pygame.K_SLASH]:
        game.move_spaceship(game.red_ship, Action.SHOOT)

    game.update()
    game.draw()

    if game.is_game_over():
        pygame.time.delay(1500)
        game.reset()

pygame.quit()
