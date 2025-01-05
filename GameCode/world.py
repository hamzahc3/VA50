import pygame as pg

class World():
    
    def __init__(self, img):
        self.img = img
    
    def draw(self, surface):
        surface.blit(self.img, (0,0))