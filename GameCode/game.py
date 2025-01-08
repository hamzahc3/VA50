import pygame as pg
from GameCode.enemy import Enemy
from GameCode.world import World
from GameCode.turret import Turret

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
# FPS = 60

# Game loop
def gameLoop(screen, world, enemyGroup, turretGroup):
    """
    The core function of the game to put inside a while loop.

    Returns:
        True if the user quits, false otherwise
    """
    over = False

    # clock.tick(FPS)

    screen.fill("grey100")

    # Draw level
    world.draw(screen)

    # Draw enemies
    enemyGroup.update()
    enemyGroup.draw(screen)
    # Turrets are handled in the main loop

    # Event handler
    for event in pg.event.get():

        # Quit program
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            over = True

    # Update display
    pg.display.flip()
    return over


# while True:
#     if gameLoop():
#         break

pg.quit()