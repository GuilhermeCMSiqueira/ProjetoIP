import pygame
from pygame.locals import *

class Bomba(pygame.sprite.Sprite):
    def __init__(self, zumbi):
        super().__init__()
        self.tamanho_x = 36
        self.tamanho_y = 60
        self.image = pygame.image.load('bomba_nuclear.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.tamanho_x, self.tamanho_y))
        self.rect = self.image.get_rect()
        self.rect.x = zumbi.rect.x + 12
        self.rect.y = zumbi.rect.y
