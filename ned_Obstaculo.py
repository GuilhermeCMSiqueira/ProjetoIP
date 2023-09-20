import pygame
from pygame.locals import *

largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, posição_x, posição_y, tamanho_x, tamanho_y):
        super().__init__()
        self.image = pygame.Surface((tamanho_x, tamanho_y))
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = posição_x
        self.rect.y = posição_y
