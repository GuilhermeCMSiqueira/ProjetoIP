import pygame
from pygame.locals import *

largura_tela = 640
altura_tela = 480
tela = pygame.display.set_mode((largura_tela, altura_tela))

class Jogador:
    def __init__(self, largura_tela, altura_tela):
        self.vida = 3
        self.tamanho = 40
        self.velocidade = 3
        self.posição_x = largura_tela/2 - self.tamanho/2
        self.posição_y = altura_tela/2 - self.tamanho/2
        self.hit_box = pygame.draw.rect(tela, (255, 255, 255), (self.posição_x, self.posição_y, self.tamanho, self.tamanho))
        
    def movimentação_jogador(self, largura_tela, altura_tela):
        if pygame.key.get_pressed()[K_a] and self.posição_x>0:
            self.posição_x -= 1*self.velocidade
        elif pygame.key.get_pressed()[K_d] and self.posição_x<(largura_tela-self.tamanho):
            self.posição_x += 1*self.velocidade
        if pygame.key.get_pressed()[K_w] and self.posição_y>0:
            self.posição_y -= 1*self.velocidade
        elif pygame.key.get_pressed()[K_s] and self.posição_y<(altura_tela-self.tamanho):
            self.posição_y += 1*self.velocidade
        self.hit_box = pygame.draw.rect(tela, (255, 255, 255), (self.posição_x, self.posição_y, self.tamanho, self.tamanho))
    
    def recebeu_mordida(self):
        self.vida -= 1
