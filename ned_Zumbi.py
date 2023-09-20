import pygame
from pygame.locals import *
from random import randint
import time

largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
#verde_musgo = (107, 142, 35)

class Zumbi(pygame.sprite.Sprite):
    def __init__(self, tamanho=40, vida=3):
        super().__init__()
        self.tamanho = tamanho
        self.image = pygame.Surface((self.tamanho, self.tamanho))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.coordenada_spawn_zumbi(largura_tela, altura_tela)
        self.vida = vida
        self.velocidade = 1
        self.tempo_recarga_total = 3
        self.tempo_ultima_mordida = 0

    def coordenada_spawn_zumbi(self, largura_tela, altura_tela):
        posição_x = randint(0-(3*self.tamanho), largura_tela+(3*self.tamanho))
        posição_y = randint(0-(3*self.tamanho), altura_tela+(3*self.tamanho))
        if posição_x<(0-self.tamanho) or posição_x>(largura_tela+self.tamanho) or posição_y<(0-self.tamanho) or posição_y>(altura_tela+self.tamanho):
            self.vida = 3
            return(posição_x, posição_y)
        else:
            return(self.coordenada_spawn_zumbi(largura_tela, altura_tela))
    
    def movimentação_zumbi(self, jogador, grupo_zumbis, grupo_obstaculo, tempo_atual):
        if self.rect.x > jogador.rect.x:
            self.rect.x -= 1*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.x += 1*self.velocidade
            if self.rect.colliderect(jogador.rect):
                self.ataque(jogador, tempo_atual)
                self.rect.x += 1*self.velocidade
            for zumbi in grupo_zumbis:
                if self!=zumbi and self.rect.colliderect(zumbi.rect):
                    if self.rect.x > zumbi.rect.x:
                        self.rect.x += 1*self.velocidade
                    else:
                        self.rect.x -= 1*self.velocidade
        elif self.rect.x < jogador.rect.x:
            self.rect.x += 1.0*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.x -= 1*self.velocidade
            if self.rect.colliderect(jogador.rect):
                self.ataque(jogador, tempo_atual)
                self.rect.x -= 1.0*self.velocidade
            for zumbi in grupo_zumbis:
                if self!=zumbi and self.rect.colliderect(zumbi.rect):
                    if self.rect.x > zumbi.rect.x:
                        self.rect.x += 1*self.velocidade
                    else:
                        self.rect.x -= 1*self.velocidade
        if self.rect.y > jogador.rect.y:
            self.rect.y -= 1.0*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.y += 1*self.velocidade
            if self.rect.colliderect(jogador.rect):
                self.ataque(jogador, tempo_atual)
                self.rect.y += 1.0*self.velocidade
            for zumbi in grupo_zumbis:
                if self!=zumbi and self.rect.colliderect(zumbi.rect):
                    if self.rect.y > zumbi.rect.y:
                        self.rect.y += 1*self.velocidade
                    else:
                        self.rect.y -= 1*self.velocidade
        elif self.rect.y < jogador.rect.y:
            self.rect.y += 1.0*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.y -= 1*self.velocidade
            if self.rect.colliderect(jogador.rect):
                self.ataque(jogador, tempo_atual)
                self.rect.y -= 1.0*self.velocidade
            for zumbi in grupo_zumbis:
                if self!=zumbi and self.rect.colliderect(zumbi.rect):
                    if self.rect.y > zumbi.rect.y:
                        self.rect.y += 1*self.velocidade
                    else:
                        self.rect.y -= 1*self.velocidade
        tela.blit(self.image, self.rect)
    
    def recebeu_tiro(self):
        self.vida -= 1
    
    def ataque(self, jogador, tempo_atual):
        if self.tempo_ultima_mordida == 0:
            jogador.recebeu_mordida()
            self.tempo_ultima_mordida = tempo_atual
        if self.tempo_ultima_mordida+self.tempo_recarga_total < tempo_atual:
            jogador.recebeu_mordida()
            self.tempo_ultima_mordida = tempo_atual
    
    def drop_kit_medico(self):
        numero_sorteado = randint(5, 100)
        lista_numeros_sorte = [7, 10, 68, 69, 88]
        if numero_sorteado in lista_numeros_sorte:
            return (True)
        else:
            return(False)
