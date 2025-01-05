import pygame as pg
from enemy import Enemy
from world import World
from turret import Turret

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60 # TODO: remove when putting it in the main loop

# Initialise pygame and the game window
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("")

# Load map
bgImg = pg.image.load("GameCode/bg.png").convert_alpha()


# Path for entities to follow
path = [
    (-50, 300),
    (310, 300),
    (310, 160),
    (990, 160),
    (990, 410),
    (710, 410),
    (710, 610),
    (1320, 610)
]

# Create enemy and group
enemyGroup = pg.sprite.Group()
turretGroup = pg.sprite.Group()

e = Enemy(path, speed=3)
enemyGroup.add(e)

world = World(bgImg)

def createTurret(mousePos):
    turret = Turret(mousePos)
    turretGroup.add(turret)

# Game loop
def gameLoop():
    """
    The core function of the game to put inside a while loop.

    Returns:
        True if the user quits, false otherwise
    """
    over = False

    clock.tick(FPS) # TODO: remove when putting it in the main loop

    screen.fill("grey100")

    # Draw level
    world.draw(screen)


    # Draw enemies
    enemyGroup.update()
    turretGroup.update(enemyGroup)
    enemyGroup.draw(screen)
    for turret in turretGroup:
        turret.draw(screen)

    # Event handler
    for event in pg.event.get():

        # Quit program
        if event.type == pg.QUIT:
            over = True

        # Mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mousePos = pg.mouse.get_pos()
            createTurret(mousePos)


    # Update display
    pg.display.flip()
    return over


while True:
    if gameLoop():
        break

pg.quit()