from typing import Any
import pygame
from pygame.locals import *
import math

largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))

class Jogador(pygame.sprite.Sprite):
    def __init__(self, largura_tela, altura_tela):
        super().__init__()
        self.tamanho = 50
        self.sprites_parado = []
        self.indice_parado = 0
        for n in range(20):
            imagem = pygame.image.load(f'sobrevivente/idle/idle_handgun_{n}.png').convert_alpha()
            imagem = pygame.transform.scale(imagem, (5*10, 5*10))
            self.sprites_parado.append(imagem)
        self.sprites_movimento = []
        self.indice_movimento = 0
        for n in range(20):
            imagem = pygame.image.load(f'sobrevivente/move/move_handgun_{n}.png').convert_alpha()
            imagem = pygame.transform.scale(imagem, (5*10, 5*10))
            self.sprites_movimento.append(imagem)
        self.image = self.sprites_movimento[int(self.indice_movimento)]
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))
        self.rect = self.image.get_rect()
        self.rect.centerx = largura_tela//2
        self.rect.centery = altura_tela//2
        self.vida = 3
        self.velocidade = 3
        self.munição_total = 15
        self.munição = self.munição_total
        self.tempo_recarga_total = 2.0
        self.tempo_recarga = 0.0
        
    def movimentação_jogador(self, largura_tela, altura_tela, grupo_zumbis, grupo_obstaculo, mouse_x, mouse_y):
        #Mecânica de movimentação do jogador
        andou = False
        if pygame.key.get_pressed()[K_a] and self.rect.x>0:
            andou = True
            self.rect.x -= 1*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.x += 1*self.velocidade
            for zumbi in grupo_zumbis:
                if self.rect.colliderect(zumbi.rect):
                    self.rect.x += 1*self.velocidade
        elif pygame.key.get_pressed()[K_d] and self.rect.x<(largura_tela-self.tamanho):
            andou = True
            self.rect.x += 1*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.x -= 1*self.velocidade
            for zumbi in grupo_zumbis:
                if self.rect.colliderect(zumbi.rect):
                    self.rect.x -= 1*self.velocidade
        if pygame.key.get_pressed()[K_w] and self.rect.y>0:
            andou = True
            self.rect.y -= 1*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.y += 1*self.velocidade
            for zumbi in grupo_zumbis:
                if self.rect.colliderect(zumbi.rect):
                    self.rect.y += 1*self.velocidade
        elif pygame.key.get_pressed()[K_s] and self.rect.y<(altura_tela-self.tamanho):
            andou = True
            self.rect.y += 1*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.y -= 1*self.velocidade
            for zumbi in grupo_zumbis:
                if self.rect.colliderect(zumbi.rect):
                    self.rect.y -= 1*self.velocidade
        #Definição da Sprite Sheet:
        if andou==True:
            self.indice_movimento += 0.5
            if self.indice_movimento >= len(self.sprites_movimento):
                self.indice_movimento = 0
            self.image = self.sprites_movimento[int(self.indice_movimento)]
        elif andou==False:
            self.indice_parado += 0.5
            if self.indice_parado >= len(self.sprites_parado):
                self.indice_parado = 0
            self.image = self.sprites_parado[int(self.indice_parado)]
        #Mecânica de Rotação do Jogador com o Mouse:
        distancia_x = mouse_x - self.rect.centerx
        distancia_y = mouse_y - self.rect.centery
        angulo_rads = math.atan2(-distancia_y, distancia_x)
        self.image = pygame.transform.rotate(self.image, math.degrees(angulo_rads))
        self.rect = self.image.get_rect(center=self.rect.center)
        for obstaculo in grupo_obstaculo:
            if self.rect.colliderect(obstaculo.rect):
                if self.rect.x > obstaculo.rect.x:
                    self.rect.x += 1
                elif self.rect.x < obstaculo.rect.x:
                    self.rect.x -= 1
                if self.rect.y > obstaculo.rect.y:
                    self.rect.y += 1
                elif self.rect.y < obstaculo.rect.y:
                    self.rect.y -= 1
        #Carregamento da imagem na tela:
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
            return(False)
        else:
            self.munição = self.munição_total
            self.tempo_recarga = 0.0
            return(True)
        
    def disparo(self, delta_time):
        self.munição -= 1
        if self.munição <= 0:
            self.recarga(delta_time)
