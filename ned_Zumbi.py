import pygame
from pygame.locals import *
from random import randint
import time

largura_tela = 640
altura_tela = 480
tela = pygame.display.set_mode((largura_tela, altura_tela))

class Zumbi:
    def __init__(self):
        self.vida = 3
        self.tamanho = 40
        self.velocidade = 1
        self.tempo_recarga = 3.0
        self.tempo_última_mordida = 0
        self.posição_x, self.posição_y = self.coordenada_spawn_zumbi(largura_tela, altura_tela)
        self.hit_box = pygame.draw.rect(tela, (107, 142, 35), (self.posição_x, self.posição_y, self.tamanho, self.tamanho))

    def coordenada_spawn_zumbi(self, largura_tela, altura_tela):
        posição_x = randint(0-(2*self.tamanho), largura_tela+(2*self.tamanho))
        posição_y = randint(0-(2*self.tamanho), altura_tela+(2*self.tamanho))
        if posição_x<(0-self.tamanho) or posição_x>(largura_tela+self.tamanho) or posição_y<(0-self.tamanho) or posição_y>(altura_tela+self.tamanho):
            return(posição_x, posição_y)
        else:
            return(self.coordenada_spawn_zumbi(largura_tela, altura_tela))
    
    def movimentação_zumbi(self, jogador):
        if self.posição_x > jogador.posição_x:
            self.posição_x -= 1*self.velocidade
        elif self.posição_x < jogador.posição_x:
            self.posição_x += 1*self.velocidade
        if self.posição_y > jogador.posição_y:
            self.posição_y -= 1*self.velocidade
        elif self.posição_y < jogador.posição_y:
            self.posição_y += 1*self.velocidade
        self.hit_box = pygame.draw.rect(tela, (107, 142, 35), (self.posição_x, self.posição_y, self.tamanho, self.tamanho))
    
    def recebeu_tiro(self):
        self.vida -= 1
    
    def ataque(self):
        cronometro = time.time()
        if cronometro - self.tempo_última_mordida >= self.tempo_recarga:
            self.tempo_última_mordida = cronometro
