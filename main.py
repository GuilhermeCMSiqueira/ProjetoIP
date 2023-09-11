import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

largura_tela = 640
altura_tela = 480

tamanho_objeto = 40
tamanho_projétil = 8  # Tamanho do projétil
velocidade_projétil = 10  # Velocidade do projétil
velocidade_zumbi = 2.5  # Velocidade do zumbi (metade da velocidade do sobrevivente)

posicao_x_sobrevivente = largura_tela / 2 - tamanho_objeto / 2
posicao_y_sobrevivente = altura_tela / 2 - tamanho_objeto / 2

fonte = pygame.font.SysFont('arial', 20, True, True)
pontos = 0
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('CInZombie')
relogio = pygame.time.Clock()

zumbi = pygame.Rect(-tamanho_objeto, randint(0, altura_tela - tamanho_objeto), tamanho_objeto, tamanho_objeto)

projeteis = []  # Lista para armazenar os projéteis disparados

quadrado_branco = pygame.Rect(300, 200, tamanho_objeto, tamanho_objeto)
mortes = 0

while True:
    relogio.tick(60)
    tela.fill((0, 0, 0))
    mensagem = f'Pontos: {pontos} Mortes: {mortes}'
    texto_pontuacao = fonte.render(mensagem, False, (255, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            # Dispare um projétil na direção do clique do mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - posicao_x_sobrevivente
            dy = mouse_y - posicao_y_sobrevivente
            dist = max(1, abs(dx) + abs(dy))
            direcao_x = dx / dist
            direcao_y = dy / dist
            projeteis.append([posicao_x_sobrevivente, posicao_y_sobrevivente, direcao_x * velocidade_projétil, direcao_y * velocidade_projétil])

    if pygame.key.get_pressed()[K_a] and posicao_x_sobrevivente > 0:
        posicao_x_sobrevivente -= 5
    elif pygame.key.get_pressed()[K_d] and posicao_x_sobrevivente < largura_tela - tamanho_objeto:
        posicao_x_sobrevivente += 5
    if pygame.key.get_pressed()[K_w] and posicao_y_sobrevivente > 0:
        posicao_y_sobrevivente -= 5
    elif pygame.key.get_pressed()[K_s] and posicao_y_sobrevivente < altura_tela - tamanho_objeto:
        posicao_y_sobrevivente += 5

    # Atualize a posição dos projéteis e verifique se eles ultrapassaram os limites da tela
    projéteis_a_remover = []
    for projétil in projeteis:
        projétil[0] += projétil[2]
        projétil[1] += projétil[3]
        if projétil[0] < 0 or projétil[0] > largura_tela or projétil[1] < 0 or projétil[1] > altura_tela:
            projéteis_a_remover.append(projétil)

    # Remova os projéteis que ultrapassaram os limites da tela
    for projétil in projéteis_a_remover:
        projeteis.remove(projétil)

    # Movimente o zumbi com metade da velocidade do sobrevivente
    direcao_x = posicao_x_sobrevivente - zumbi.x
    direcao_y = posicao_y_sobrevivente - zumbi.y
    dist = max(1, abs(direcao_x) + abs(direcao_y))
    direcao_x /= dist
    direcao_y /= dist
    zumbi.x += direcao_x * velocidade_zumbi
    zumbi.y += direcao_y * velocidade_zumbi

    # Verifique se o zumbi atingiu os limites da tela e reposicione-o
    if zumbi.right < 0:
        zumbi.left = largura_tela
        zumbi.top = randint(0, altura_tela - tamanho_objeto)

    # Desenhe o sobrevivente
    sobrevivente = pygame.draw.rect(tela, (255, 255, 255), (posicao_x_sobrevivente, posicao_y_sobrevivente, tamanho_objeto, tamanho_objeto))

    # Desenhe os projéteis
    for projétil in projeteis:
        pygame.draw.rect(tela, (255, 0, 0), (projétil[0], projétil[1], tamanho_projétil, tamanho_projétil))

    # Desenhe o zumbi
    pygame.draw.rect(tela, (107, 142, 35), zumbi)

    # Verifique colisão entre projéteis e zumbi
    projéteis_a_remover = []
    for projétil in projeteis:
        projétil_rect = pygame.Rect(projétil[0], projétil[1], tamanho_projétil, tamanho_projétil)
        if projétil_rect.colliderect(zumbi):
            projéteis_a_remover.append(projétil)
            zumbi.left = largura_tela
            zumbi.top = randint(0, altura_tela - tamanho_objeto)
            pontos += 1

    # Remova os projéteis que colidiram com o zumbi
    for projétil in projéteis_a_remover:
        projeteis.remove(projétil)

    tela.blit(texto_pontuacao, (415, 10))
    pygame.display.update()