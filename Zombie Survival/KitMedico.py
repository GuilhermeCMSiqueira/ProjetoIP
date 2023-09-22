import pygame
from pygame.locals import *

class KitMedico(pygame.sprite.Sprite):
    def __init__(self, zumbi):
        super().__init__()
        self.tamanho = 30
        self.image = pygame.image.load('kit_medico.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))
        self.rect = self.image.get_rect()
        self.rect.center = zumbi.rect.center
        self.tempo_drop = pygame.time.get_ticks()/1000
        self.tempo_duração = 12.0

    def temporizador(self):
        cronometro = pygame.time.get_ticks()/1000
        if cronometro - self.tempo_drop >= self.tempo_duração:
            self.kill()