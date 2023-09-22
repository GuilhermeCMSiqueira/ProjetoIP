import pygame
from pygame.locals import *

largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))

class Jogador(pygame.sprite.Sprite):
    def __init__(self, largura_tela, altura_tela):
        super().__init__()
        self.tamanho = 40
        self.image = pygame.Surface((self.tamanho, self.tamanho))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = largura_tela/2 - self.tamanho/2
        self.rect.y = altura_tela/2 - self.tamanho/2
        self.vida = 3
        self.velocidade = 3
        self.munição_total = 15
        self.munição = self.munição_total
        self.tempo_recarga_total = 2.0
        self.tempo_recarga = 0.0
        
    def movimentação_jogador(self, largura_tela, altura_tela, grupo_zumbis, grupo_obstaculo):
        if pygame.key.get_pressed()[K_a] and self.rect.x>0:
            self.rect.x -= 1*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.x += 1*self.velocidade
            for zumbi in grupo_zumbis:
                if self.rect.colliderect(zumbi.rect):
                    self.rect.x += 1*self.velocidade
        elif pygame.key.get_pressed()[K_d] and self.rect.x<(largura_tela-self.tamanho):
            self.rect.x += 1*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.x -= 1*self.velocidade
            for zumbi in grupo_zumbis:
                if self.rect.colliderect(zumbi.rect):
                    self.rect.x -= 1*self.velocidade
        if pygame.key.get_pressed()[K_w] and self.rect.y>0:
            self.rect.y -= 1*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.y += 1*self.velocidade
            for zumbi in grupo_zumbis:
                if self.rect.colliderect(zumbi.rect):
                    self.rect.y += 1*self.velocidade
        elif pygame.key.get_pressed()[K_s] and self.rect.y<(altura_tela-self.tamanho):
            self.rect.y += 1*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.y -= 1*self.velocidade
            for zumbi in grupo_zumbis:
                if self.rect.colliderect(zumbi.rect):
                    self.rect.y -= 1*self.velocidade
        tela.blit(self.image, self.rect)
    
    def recebeu_mordida(self):
        self.vida -= 1
    
    def pegou_kitmedico(self):
        if self.vida < 3:
            self.vida += 1

    def recarga(self, delta_time):
        if self.tempo_recarga < self.tempo_recarga_total:
            self.munição = 0
            self.tempo_recarga += delta_time
        else:
            self.munição = self.munição_total
            self.tempo_recarga = 0.0
    
    def disparo(self, delta_time):
        self.munição -= 1
        if self.munição <= 0:
            self.recarga(delta_time)