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
            tamanho = random.randint(40, 40)
            velocidade = 1
            zumbi = cls(tipo, tamanho, velocidade)
            zumbis.append(zumbi)
        return zumbis

class Projetil:
    tamanho_projetil = 10
    velocidade_projetil = 5
    cor_projetil = verde

    def __init__(self, x, y, direcao_x, direcao_y):
        self.x = x
        self.y = y
        self.direcao_x = direcao_x
        self.direcao_y = direcao_y

    def mover(self):
        self.x += self.direcao_x * self.velocidade_projetil
        self.y += self.direcao_y * self.velocidade_projetil

    def desenhar(self):
        pygame.draw.rect(tela, self.cor_projetil, (self.x - self.tamanho_projetil // 2, self.y, self.tamanho_projetil, self.tamanho_projetil))
