import pygame as pg
import math

class Turret(pg.sprite.Sprite):
    """
    Turret class.

    Initialisation:
        pos (int tuple): Where the tower is set
        range (int): Max range of the tower to detect enemies (default: 280)
        damage (int): Damage dealt to enemies it targets (default: 5)

    Methods:
        draw(Surface): Draws the turret and its range circle on the given surface
        pickTarget(enemyGroup): Checks all enemies targets the first one in its range
        shoot(enemy): Deals self.damage to the target enemy
        update(): Shoots its current target, picks a target if none are current
    """
    
    def __init__(self, pos, range=280, damage=5):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("GameCode/enemySprite.png").convert_alpha()
        self.damage = damage

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.target = None

        # Create range circle
        self.range = range
        self.rangeImg = pg.Surface((self.range*2, self.range*2))
        self.rangeImg.fill((0,0,0))
        self.rangeImg.set_colorkey((0,0,0))
        pg.draw.circle(self.rangeImg, "grey100", (self.range, self.range), self.range)
        self.rangeImg.set_alpha(100)
        self.rangeRect = self.rangeImg.get_rect()
        self.rangeRect.center = self.rect.center


    def update(self, enemyGroup):
        if self.target:
            self.shoot(self.target)
            self.target = None
        else:
            self.pickTarget(enemyGroup)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.rangeImg, self.rangeRect)

    def pickTarget(self, enemyGroup):
        
        xDis, yDist = 0, 0
        # Check 
        for enemy in enemyGroup:
            xDist = enemy.pos[0] - self.rect.center[0]
            yDist = enemy.pos[1] - self.rect.center[1]
            dist = math.sqrt(xDist**2 + yDist**2)
            if dist < self.range:
                self.target = enemy
                break

    def shoot(self, enemy):
        enemy.takeDamage(self.damage)