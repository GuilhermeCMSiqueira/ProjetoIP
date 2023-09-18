import random
import pygame
import math
import Projetil

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))

preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)


class Sobrevivente:
    def __init__(self):
        self.x = largura // 2
        self.y = altura // 2
        self.tamanho = 30
        self.velocidade = 1.5
        self.projeteis = []

    def mover(self, direcao):
        if direcao == "esquerda" and self.x > 0:
            self.x -= self.velocidade
        elif direcao == "direita" and self.x < largura - self.tamanho:
            self.x += self.velocidade
        elif direcao == "cima" and self.y > 0:
            self.y -= self.velocidade
        elif direcao == "baixo" and self.y < altura - self.tamanho:
            self.y += self.velocidade


    def atirar(self, mouse_x, mouse_y):
        # Calcula a direção do mouse em relação ao Sobrevivente
        direcao_x = mouse_x - self.x
        direcao_y = mouse_y - self.y

        # Calcula o comprimento do vetor direção
        comprimento = math.sqrt(direcao_x ** 2 + direcao_y ** 2)

        # Normaliza a direção para ter um comprimento de 1
        if comprimento != 0:
            direcao_x /= comprimento
            direcao_y /= comprimento

        # Cria um novo projétil na posição do Sobrevivente com a direção calculada
        novo_projétil = Projetil(self.x + self.tamanho // 2, self.y, direcao_x, direcao_y)
        self.projeteis.append(novo_projétil)


    def desenhar(self):
        pygame.draw.rect(tela, preto, (self.x, self.y, self.tamanho, self.tamanho))
