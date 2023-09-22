import pygame
from pygame.locals import *

largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))

class Projetil(pygame.sprite.Sprite):
    def __init__(self, mouse_x, mouse_y, jogador, delta_time):
        super().__init__()
        jogador.disparo(delta_time)
        self.tamanho = 5
        self.image = pygame.Surface((self.tamanho, self.tamanho))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = jogador.rect.x + jogador.tamanho/2
        self.rect.y = jogador.rect.y + jogador.tamanho/2
        self.vetor_x, self.vetor_y = self.calculo_vetor(mouse_x, mouse_y, jogador)
        self.velocidade = 10

    def calculo_vetor(self, mouse_x, mouse_y, jogador):
        distancia_x = mouse_x - (jogador.rect.x + jogador.tamanho/2)
        distancia_y = mouse_y - (jogador.rect.y + jogador.tamanho/2)
        distancia_total = max(1, abs(distancia_x) + abs(distancia_y))
        vetor_x = distancia_x / distancia_total
        vetor_y = distancia_y / distancia_total
        return(vetor_x, vetor_y)

    def movimentação_projetil(self, grupo_zumbis):
        self.rect.x += self.vetor_x*self.velocidade
        self.rect.y += self.vetor_y*self.velocidade
        for zumbi in grupo_zumbis:
            if self.rect.colliderect(zumbi.rect):
                zumbi.recebeu_tiro()
                self.kill()
        tela.blit(self.image, self.rect)