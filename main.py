import pygame
from pygame.locals import *
from sys import exit
from random import randint, choice
import time

pygame.init()

largura_tela = 840
altura_tela = 680

tamanho_objeto = 40
tamanho_projétil = 8
velocidade_projétil = 10
velocidade_zumbi = 2.3

fonte = pygame.font.SysFont('arial', 20, True, True)
pontos = {'verde': 0, 'vermelho': 0, 'azul': 0}  # Contadores de pontos para cada tipo de zumbi
mortes = 0
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('CInZombie')
relogio = pygame.time.Clock()

sobrevivente = pygame.Rect(largura_tela / 2 - tamanho_objeto / 2, altura_tela / 2 - tamanho_objeto / 2, tamanho_objeto,
                           tamanho_objeto)
projeteis = []


def criar_zumbi():
    lado = randint(1, 4)
    if lado == 1:
        x = -tamanho_objeto
        y = randint(0, altura_tela - tamanho_objeto)
    elif lado == 2:
        x = largura_tela
        y = randint(0, altura_tela - tamanho_objeto)
    elif lado == 3:
        x = randint(0, largura_tela - tamanho_objeto)
        y = -tamanho_objeto
    else:
        x = randint(0, largura_tela - tamanho_objeto)
        y = altura_tela
    cor = choice(['verde', 'vermelho', 'azul'])  # Tipos de zumbi: verde, vermelho, azul
    return pygame.Rect(x, y, tamanho_objeto, tamanho_objeto), cor


zumbis = []  # Lista de zumbis

for _ in range(3):  # Cria três zumbis com cores diferentes
    zumbi, cor = criar_zumbi()
    zumbis.append((zumbi, cor))

cores = {'verde': (0, 255, 0), 'vermelho': (255, 0, 0),
         'azul': (0, 0, 255)}  # Mapeamento de cores para cada tipo de zumbi

# Variáveis do cronômetro
tempo_inicial = time.time()
tempo_limite = 60  # 60 segundos
tempo_restante = tempo_limite

while True:
    relogio.tick(60)
    tela.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - sobrevivente.x
            dy = mouse_y - sobrevivente.y
            dist = max(1, abs(dx) + abs(dy))
            direcao_x = dx / dist
            direcao_y = dy / dist
            projeteis.append(
                [sobrevivente.x, sobrevivente.y, direcao_x * velocidade_projétil, direcao_y * velocidade_projétil])

    keys = pygame.key.get_pressed()
    if keys[K_a] and sobrevivente.left > 0:
        sobrevivente.x -= 5
    elif keys[K_d] and sobrevivente.right < largura_tela:
        sobrevivente.x += 5
    if keys[K_w] and sobrevivente.top > 0:
        sobrevivente.y -= 5
    elif keys[K_s] and sobrevivente.bottom < altura_tela:
        sobrevivente.y += 5

    for i, (zumbi, cor) in enumerate(zumbis):
        direcao_x = sobrevivente.x - zumbi.x
        direcao_y = sobrevivente.y - zumbi.y
        dist = max(1, abs(direcao_x) + abs(direcao_y))
        direcao_x /= dist
        direcao_y /= dist
        zumbi.x += direcao_x * velocidade_zumbi
        zumbi.y += direcao_y * velocidade_zumbi

        if zumbi.left > largura_tela or zumbi.right < 0 or zumbi.top > altura_tela or zumbi.bottom < 0:
            zumbis[i] = (criar_zumbi())

        pygame.draw.rect(tela, cores[cor], zumbi)  # Desenhe o zumbi preenchido com a cor

    projéteis_a_remover = []
    for projétil in projeteis:
        projétil[0] += projétil[2]
        projétil[1] += projétil[3]
        if projétil[0] < 0 or projétil[0] > largura_tela or projétil[1] < 0 or projétil[1] > altura_tela:
            projéteis_a_remover.append(projétil)

    for projétil in projéteis_a_remover:
        projeteis.remove(projétil)

    projéteis_a_remover = []
    for projétil in projeteis:
        projétil_rect = pygame.Rect(projétil[0], projétil[1], tamanho_projétil, tamanho_projétil)
        for i, (zumbi, cor) in enumerate(zumbis):
            if projétil_rect.colliderect(zumbi):
                projéteis_a_remover.append(projétil)
                zumbis[i] = (criar_zumbi())
                pontos[cor] += 1  # Incrementa o contador de pontos para a cor do zumbi

    for projétil in projéteis_a_remover:
        projeteis.remove(projétil)

    # Verifique colisão entre zumbis e sobrevivente
    for i, (zumbi, _) in enumerate(zumbis):
        if sobrevivente.colliderect(zumbi):
            mortes += 1  # Incrementa o contador de mortes
            zumbis[i] = (criar_zumbi())  # Reposiciona o zumbi

    pygame.draw.rect(tela, (255, 255, 255), sobrevivente)

    # Calcula o tempo restante
    tempo_atual = time.time()
    tempo_restante = max(0, tempo_limite - (tempo_atual - tempo_inicial))

    # Renderize os contadores de pontos centralizados na parte superior da tela
    mensagem_verde = fonte.render(f'Verde: {pontos["verde"]}', False, (0, 255, 0))
    mensagem_vermelho = fonte.render(f'Vermelho: {pontos["vermelho"]}', False, (255, 0, 0))
    mensagem_azul = fonte.render(f'Azul: {pontos["azul"]}', False, (0, 0, 255))

    tela.blit(mensagem_verde, (largura_tela // 2 - mensagem_verde.get_width() // 2, 10))
    tela.blit(mensagem_vermelho, (largura_tela // 2 - mensagem_vermelho.get_width() // 2, 40))
    tela.blit(mensagem_azul, (largura_tela // 2 - mensagem_azul.get_width() // 2, 70))

    # Renderize o contador de mortes centralizado na parte superior da tela
    mensagem_mortes = fonte.render(f'Mortes: {mortes}', False, (255, 255, 255))
    tela.blit(mensagem_mortes, (largura_tela // 2 - mensagem_mortes.get_width() // 2, 100))

    # Renderize o cronômetro na parte superior da tela
    mensagem_tempo = fonte.render(f'Tempo: {int(tempo_restante)}s', False, (255, 255, 255))
    tela.blit(mensagem_tempo, (largura_tela // 2 - mensagem_tempo.get_width() // 2, 130))

    # Verifique as condições de vitória e derrota
    if mortes >= 3:
        mensagem_perdeu = fonte.render('Você perdeu!', False, (255, 0, 0))
        tela.blit(mensagem_perdeu, (
        largura_tela // 2 - mensagem_perdeu.get_width() // 2, altura_tela // 2 - mensagem_perdeu.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(5000)  # Aguarde 5 segundos
        pygame.quit()
        exit()
    elif tempo_restante <= 0:
        mensagem_ganhou = fonte.render('Você ganhou!', False, (0, 255, 0))
        tela.blit(mensagem_ganhou, (
        largura_tela // 2 - mensagem_ganhou.get_width() // 2, altura_tela // 2 - mensagem_ganhou.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(5000)  # Aguarde 5 segundos
        pygame.quit()
        exit()

    # Desenhe os projéteis após desenhar os zumbis para que eles apareçam na parte superior
    for projétil in projeteis:
        pygame.draw.rect(tela, (255, 0, 0), (projétil[0], projétil[1], tamanho_projétil, tamanho_projétil))

    pygame.display.update()