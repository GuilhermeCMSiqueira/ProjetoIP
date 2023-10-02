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
            imagem = pygame.image.load(f'sobrevivente_sprite_sheet.png').subsurface((215*n, 0),(215, 215)).convert_alpha()
            imagem = pygame.transform.scale(imagem, (self.tamanho, self.tamanho))
            self.sprites_parado.append(imagem)
        self.sprites_movimento = []
        self.indice_movimento = 0
        for n in range(20):
            imagem = pygame.image.load(f'sobrevivente_sprite_sheet.png').subsurface((215*n, 215),(215, 215)).convert_alpha()
            imagem = pygame.transform.scale(imagem, (self.tamanho, self.tamanho))
            self.sprites_movimento.append(imagem)
        self.sprites_recarga = []
        self.indice_recarga = 0
        for n in range(15):
            imagem = pygame.image.load(f'sobrevivente_sprite_sheet.png').subsurface((215*n, 215*2),(215, 215)).convert_alpha()
            imagem = pygame.transform.scale(imagem, (self.tamanho, self.tamanho))
            self.sprites_recarga.append(imagem)
        self.sprites_tiro = []
        self.indice_tiro = 0
        for n in range(3):
            imagem = pygame.image.load(f'sobrevivente_sprite_sheet.png').subsurface((215*n, 215*3),(215, 215)).convert_alpha()
            imagem = pygame.transform.scale(imagem, (self.tamanho, self.tamanho))
            self.sprites_tiro.append(imagem)
        self.image = self.sprites_parado[int(self.indice_movimento)]
        self.rect = self.image.get_rect()
        self.rect.centerx = largura_tela//2
        self.rect.centery = altura_tela//2
        self.vida = 3
        self.velocidade = 3
        self.munição_total = 15
        self.munição = self.munição_total
        self.tempo_recarga_total = 2.0
        self.tempo_recarga = 0.0
        self.atirando = False
        
    def movimentação_jogador(self, largura_tela, altura_tela, grupo_zumbis, grupo_obstaculo, mouse_x, mouse_y):
        #Mecânica de movimentação do jogador
        andou = False
        if pygame.key.get_pressed()[K_a] and self.rect.left>0:
            andou = True
            self.rect.x -= 1*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.x += 1*self.velocidade
            for zumbi in grupo_zumbis:
                if self.rect.colliderect(zumbi.rect):
                    self.rect.x += 1*self.velocidade
        elif pygame.key.get_pressed()[K_d] and self.rect.right<largura_tela:
            andou = True
            self.rect.x += 1*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.x -= 1*self.velocidade
            for zumbi in grupo_zumbis:
                if self.rect.colliderect(zumbi.rect):
                    self.rect.x -= 1*self.velocidade
        if pygame.key.get_pressed()[K_w] and self.rect.top>0:
            andou = True
            self.rect.y -= 1*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.y += 1*self.velocidade
            for zumbi in grupo_zumbis:
                if self.rect.colliderect(zumbi.rect):
                    self.rect.y += 1*self.velocidade
        elif pygame.key.get_pressed()[K_s] and self.rect.bottom<altura_tela:
            andou = True
            self.rect.y += 1*self.velocidade
            for obstaculo in grupo_obstaculo:
                if self.rect.colliderect(obstaculo.rect):
                    self.rect.y -= 1*self.velocidade
            for zumbi in grupo_zumbis:
                if self.rect.colliderect(zumbi.rect):
                    self.rect.y -= 1*self.velocidade
        #Definição da Sprite Sheet:
        if self.atirando==True:
            self.image = self.sprites_tiro[int(self.indice_tiro)]
            self.indice_tiro += 0.5
            if self.indice_tiro >= len(self.sprites_tiro):
                self.indice_tiro = 0
                self.atirando = False
        elif self.munição==0:
            self.image = self.sprites_recarga[int(self.indice_recarga)]
            self.indice_recarga += 0.12
            if self.indice_recarga >= len(self.sprites_recarga):
                self.indice_recarga = 0
        elif andou==True:
            self.image = self.sprites_movimento[int(self.indice_movimento)]
            self.indice_movimento += 1
            if self.indice_movimento >= len(self.sprites_movimento):
                self.indice_movimento = 0
        else:
            self.image = self.sprites_parado[int(self.indice_parado)]
            self.indice_parado += 0.2
            if self.indice_parado >= len(self.sprites_parado):
                self.indice_parado = 0
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
            self.velocidade = 2
            return(False)
        else:
            self.munição = self.munição_total
            self.tempo_recarga = 0.0
            self.indice_recarga = 0
            self.velocidade = 3
            return(True)
        
    def disparo(self, mouse_x, mouse_y, grupo_projeteis, Projetil):
        if self.atirando==False:
            self.munição -= 1
            self.atirando = True
            novo_projetil = Projetil(mouse_x, mouse_y, self)
            grupo_projeteis.add(novo_projetil)
            
