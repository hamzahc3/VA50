import pygame as pg
from pygame.math import Vector2
import math

class Enemy(pg.sprite.Sprite):
    """
    The enemy entites of the game.
    Inherits from the pygame Sprite class.

    Attributes:
        path (list of int tuples): The waypoints of the path the entity follows
        health (int): The entity's current health (Has a default option)
        speed (float): The entity's moving speed (Has a default option)
        image: The enemy's sprite (Has a default option)

    Methods:
        move(path): Makes the enemy follow the path
    """

    def __init__(self, path, health=10, speed=1, image=None):
        pg.sprite.Sprite.__init__(self)

        # If no image is given, we use the base sprite
        if image == None:
            # Load image
            image = pg.image.load("GameCode/enemySprite.png").convert_alpha()

        self.path = path
        self.pos = Vector2(self.path[0])
        self.targetWaypoint = 1

        self.ogImage = image # Image to go back to when rotation resets
        self.angle = 0
        self.image = pg.transform.rotate(self.ogImage, self.angle)

        self.health = health
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def update(self):
        self.move()
        self.rotate()

    def move(self):
        """
        Makes the entity move along the path with a waypoint system.
        """
        if self.targetWaypoint < len(self.path):
            # Define target waypoint
            self.target = Vector2(self.path[self.targetWaypoint])
            self.movement = self.target - self.pos
        else:
            # End of path reached
            self.kill()
        
        # Check distance to target
        dist = self.movement.length()
        # Compare to speed if there is enough distance remaining
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.targetWaypoint += 1

        self.rect.center = self.pos
    
    def rotate(self):
        """
        Rotates the sprite depending on the movement direction.
        """
        dist = self.target - self.pos
        self.angle = math.degrees(math.atan2(-dist[1], dist[0])) + 90

        # Rotate the image
        # No need to update the rect because square image
        self.image = pg.transform.rotate(self.ogImage, self.angle)

    def takeDamage(self, amount):
        """
        Updates  the entity's health depending on a specified amounts.

        Params:
            amount (int): The amount of damage dealt to the entity

        Return:
            True if the entity is out of health, False otherwise
        """
        self.health -= amount
        if self.health < 0:
            self.kill()
            return True
        return False
