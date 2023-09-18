import random
import pygame
import math

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))

preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)

class Zumbi:
    def __init__(self, tipo, tamanho, velocidade):
        self.tipo = tipo
        self.tamanho = tamanho
        self.velocidade = velocidade
        self.vida = 1
        self.spawn_fora_tela()

    def spawn_fora_tela(self):
        # Gera uma posição aleatória nos limites da tela
        borda = random.choice(["cima", "baixo", "esquerda", "direita"])
        if borda == "cima":
            self.x = random.randint(0, largura - self.tamanho)
            self.y = -self.tamanho
        elif borda == "baixo":
            self.x = random.randint(0, largura - self.tamanho)
            self.y = altura
        elif borda == "esquerda":
            self.x = -self.tamanho
            self.y = random.randint(0, altura - self.tamanho)
        elif borda == "direita":
            self.x = largura
            self.y = random.randint(0, altura - self.tamanho)

    def seguir_sobrevivente(self, sobrevivente):
        dx = sobrevivente.x - self.x
        dy = sobrevivente.y - self.y
        distancia = math.sqrt(dx ** 2 + dy ** 2)
        if distancia != 0:
            dx = dx / distancia
            dy = dy / distancia
        self.x += dx * self.velocidade
        self.y += dy * self.velocidade

    def desenhar(self):
        if self.tipo == "azul":
            pygame.draw.rect(tela, azul, (self.x, self.y, self.tamanho, self.tamanho))
        elif self.tipo == "verde":
            pygame.draw.rect(tela, verde, (self.x, self.y, self.tamanho, self.tamanho))
        elif self.tipo == "vermelho":
            pygame.draw.rect(tela, vermelho, (self.x, self.y, self.tamanho, self.tamanho))

    @classmethod
    def criar_zumbis(cls, num_zumbis):
        zumbis = []
        for c in range(num_zumbis):
            tipo = random.choice(["azul", "verde", "vermelho"])
            tamanho = 40
            velocidade = 1
            zumbi = cls(tipo, tamanho, velocidade)
            zumbis.append(zumbi)
        return zumbis
