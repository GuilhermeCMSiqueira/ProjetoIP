import pygame
from pygame.locals import *

largura_tela = 640
altura_tela = 480
tela = pygame.display.set_mode((largura_tela, altura_tela))

class Projetil:
    def __init__(self, jogador, vetor_x, vetor_y):
        self.tamanho = 5
        self.velocidade = 10
        self.posição_x = jogador.posição_x + jogador.tamanho/2
        self.posição_y = jogador.posição_y + jogador.tamanho/2
        self.vetor_x = vetor_x
        self.vetor_y = vetor_y
        self.hit_box = pygame.draw.rect(tela, (255, 0, 0), (self.posição_x, self.posição_y, self.tamanho, self.tamanho))

    def movimentação_projetil(self):
        self.posição_x += self.vetor_x*self.velocidade
        self.posição_y += self.vetor_y*self.velocidade
        self.hit_box = pygame.draw.rect(tela, (255, 0, 0), (self.posição_x, self.posição_y, self.tamanho, self.tamanho))
