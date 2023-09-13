import pygame
from pygame.locals import *
from sys import exit
from random import randint, choice
import time

class Zumbi:
    def __init__(self, tela, tamanho_objeto, largura_tela, altura_tela):
        self.tela = tela
        self.tamanho_objeto = tamanho_objeto
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.rect, self.cor = self.criar_zumbi()
    
    def criar_zumbi(self):
        lado = randint(1, 4)
        if lado == 1:
            x = -self.tamanho_objeto
            y = randint(0, self.altura_tela - self.tamanho_objeto)
        elif lado == 2:
            x = self.largura_tela
            y = randint(0, self.altura_tela - self.tamanho_objeto)
        elif lado == 3:
            x = randint(0, self.largura_tela - self.tamanho_objeto)
            y = -self.tamanho_objeto
        else:
            x = randint(0, self.largura_tela - self.tamanho_objeto)
            y = self.altura_tela
        cor = choice(['verde', 'vermelho', 'azul'])  # Tipos de zumbi: verde, vermelho, azul
        return pygame.Rect(x, y, self.tamanho_objeto, self.tamanho_objeto), cor

class Projétil:
    def __init__(self, tela, x, y, direcao_x, direcao_y, tamanho_projétil):
        self.tela = tela
        self.rect = pygame.Rect(x, y, tamanho_projétil, tamanho_projétil)
        self.direcao_x = direcao_x
        self.direcao_y = direcao_y

class Sobrevivente:
    def __init__(self, largura_tela, altura_tela, tamanho_objeto):
        self.rect = pygame.Rect(largura_tela / 2 - tamanho_objeto / 2, altura_tela / 2 - tamanho_objeto / 2, tamanho_objeto, tamanho_objeto)

class Jogo:
    def __init__(self):
        pygame.init()

        self.largura_tela = 640
        self.altura_tela = 480

        self.tamanho_objeto = 40
        self.tamanho_projetil = 8
        self.velocidade_projetil = 10
        self.velocidade_zumbi = 3

        self.fonte = pygame.font.SysFont('arial', 20, True, True)
        self.pontos = {'verde': 0, 'vermelho': 0, 'azul': 0}  # Contadores de pontos para cada tipo de zumbi
        self.mortes = 0
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        pygame.display.set_caption('CInZombie')
        self.relogio = pygame.time.Clock()

        self.sobrevivente = Sobrevivente(self.largura_tela, self.altura_tela, self.tamanho_objeto)
        self.projeteis = []

        self.zumbis = []  # Lista de zumbis

        for _ in range(5):  # Cria três zumbis com cores diferentes
            zumbi = Zumbi(self.tela, self.tamanho_objeto, self.largura_tela, self.altura_tela)
            self.zumbis.append(zumbi)

        self.cores = {'verde': (0, 255, 0), 'vermelho': (255, 0, 0), 'azul': (0, 0, 255)}  # Mapeamento de cores para cada tipo de zumbi

        # Variáveis do cronômetro
        self.tempo_inicial = time.time()
        self.tempo_limite = 60  
        self.tempo_restante = self.tempo_limite

    def executar(self):
        projeteis=[]
        while True:
            self.relogio.tick(60)
            self.tela.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dx = mouse_x - self.sobrevivente.rect.x
                    dy = mouse_y - self.sobrevivente.rect.y
                    dist = max(1, abs(dx) + abs(dy))
                    direcao_x = dx / dist
                    direcao_y = dy / dist
                    self.projeteis.append(Projétil(self.tela, self.sobrevivente.rect.x, self.sobrevivente.rect.y, direcao_x * self.velocidade_projetil, direcao_y * self.velocidade_projetil, self.tamanho_projetil))

            keys = pygame.key.get_pressed()
            if keys[K_a] and self.sobrevivente.rect.left > 0:
                self.sobrevivente.rect.x -= 5
            elif keys[K_d] and self.sobrevivente.rect.right < self.largura_tela:
                self.sobrevivente.rect.x += 5
            if keys[K_w] and self.sobrevivente.rect.top > 0:
                self.sobrevivente.rect.y -= 5
            elif keys[K_s] and self.sobrevivente.rect.bottom < self.altura_tela:
                self.sobrevivente.rect.y += 5

            for i, zumbi in enumerate(self.zumbis):
                direcao_x = self.sobrevivente.rect.x - zumbi.rect.x
                direcao_y = self.sobrevivente.rect.y - zumbi.rect.y
                dist = max(1, abs(direcao_x) + abs(direcao_y))
                direcao_x /= dist
                direcao_y /= dist
                zumbi.rect.x += direcao_x * self.velocidade_zumbi
                zumbi.rect.y += direcao_y * self.velocidade_zumbi

                if zumbi.rect.left > self.largura_tela or zumbi.rect.right < 0 or zumbi.rect.top > self.altura_tela or zumbi.rect.bottom < 0:
                    self.zumbis[i] = Zumbi(self.tela, self.tamanho_objeto, self.largura_tela, self.altura_tela)

                pygame.draw.rect(self.tela, self.cores[zumbi.cor], zumbi.rect)  # Desenhe o zumbi preenchido com a cor

            projeteis_a_remover = []
            for projetil in self.projeteis:
                projetil.rect.x += projetil.direcao_x
                projetil.rect.y += projetil.direcao_y
                if projetil.rect.x < 0 or projetil.rect.x > self.largura_tela or projetil.rect.y < 0 or projetil.rect.y > self.altura_tela:
                    projeteis_a_remover.append(projetil)

            for projetil in projeteis_a_remover:
                self.projeteis.remove(projetil)

            projeteis_a_remover = []
            for projetil in self.projeteis:
                projetil_rect = projetil.rect
                for i, zumbi in enumerate(self.zumbis):
                    if projetil_rect.colliderect(zumbi.rect):
                        projeteis_a_remover.append(projetil)
                        self.zumbis[i] = Zumbi(self.tela, self.tamanho_objeto, self.largura_tela, self.altura_tela)
                        self.pontos[zumbi.cor] += 1  # Incrementa o contador de pontos para a cor do zumbi

            for projetil in projeteis_a_remover:
                if(projetil in self.projeteis):
                    self.projeteis.remove(projetil)

            # Verifique colisão entre zumbis e sobrevivente
            for i, zumbi in enumerate(self.zumbis):
                if self.sobrevivente.rect.colliderect(zumbi.rect):
                    self.mortes += 1  # Incrementa o contador de mortes
                    self.zumbis[i] = Zumbi(self.tela, self.tamanho_objeto, self.largura_tela, self.altura_tela)  # Reposiciona o zumbi

            # Renderize a linha de pontos na parte superior da tela
            linha_pontuacao_x = (self.largura_tela - (20 + sum([self.fonte.render(f'{cor.capitalize()}: {self.pontos[cor]}', False, self.cores[cor]).get_width() for cor in self.pontos]))) // 2
            for cor in self.pontos:
                mensagem_pontos = self.fonte.render(f'{cor.capitalize()}: {self.pontos[cor]}', False, self.cores[cor])
                self.tela.blit(mensagem_pontos, (linha_pontuacao_x, 10))
                linha_pontuacao_x += mensagem_pontos.get_width() + 10

            mensagem_mortes = self.fonte.render(f'Mortes: {self.mortes}', False, (255, 255, 255))
            mensagem_tempo = self.fonte.render(f'Tempo: {int(self.tempo_restante)}s', False, (255, 255, 255))

            largura_total = mensagem_mortes.get_width() + mensagem_tempo.get_width() + 10

            x_mortes = (self.largura_tela - largura_total) // 2
            x_tempo = x_mortes + mensagem_mortes.get_width() + 10

            self.tela.blit(mensagem_mortes, (x_mortes, 40))
            self.tela.blit(mensagem_tempo, (x_tempo, 40))
            # Renderize o contador de mortes centralizado na parte superior da tela
            

            # Renderize o cronômetro na parte superior da tela
            tempo_atual = time.time()
            self.tempo_restante = max(0, self.tempo_limite - (tempo_atual - self.tempo_inicial))
            mensagem_tempo = self.fonte.render(f'Tempo: {int(self.tempo_restante)}s', False, (255, 255, 255))
            

            # Verifique as condições de vitória e derrota
            if self.mortes >= 3:
                mensagem_perdeu = self.fonte.render('Você perdeu!', False, (255, 0, 0))
                self.tela.blit(mensagem_perdeu, (self.largura_tela // 2 - mensagem_perdeu.get_width() // 2, self.altura_tela // 2 - mensagem_perdeu.get_height() // 2))
                pygame.display.update()
                pygame.time.delay(5000)  # Aguarde 5 segundos
                pygame.quit()
                exit()
            elif self.tempo_restante <= 0:
                mensagem_ganhou = self.fonte.render('Você ganhou!', False, (0, 255, 0))
                self.tela.blit(mensagem_ganhou, (self.largura_tela // 2 - mensagem_ganhou.get_width() // 2, self.altura_tela // 2 - mensagem_ganhou.get_height() // 2))
                pygame.display.update()
                pygame.time.delay(5000)  # Aguarde 5 segundos
                pygame.quit()
                exit()

            # Desenhe os projéteis após desenhar os zumbis para que eles apareçam na parte superior
            for projetil in self.projeteis:
                pygame.draw.rect(self.tela, (255, 0, 0), projetil.rect)

            pygame.draw.rect(self.tela, (255, 255, 255), self.sobrevivente.rect)

            pygame.display.update()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
