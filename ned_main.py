import pygame
from pygame.locals import *
from sys import exit
from random import randint
from Jogador import Jogador
from Projetil import Projetil
from Zumbi import Zumbi

pygame.init()

#Configurações da Janela:
largura_tela = 640
altura_tela = 480
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('CInZombie')



fonte = pygame.font.SysFont('arial', 40, True, True)
quantidade_abates = 0
relogio = pygame.time.Clock()

pygame.mouse.set_visible(False)
imagem_mira = pygame.image.load('mira.png').convert_alpha()
imagem_mira = pygame.transform.scale(imagem_mira, (40, 40))
mira_rect = imagem_mira.get_rect()

jogador = Jogador(largura_tela, altura_tela)
lista_projeteis = []
zumbi0 = Zumbi()
zumbi1 = Zumbi()
zumbi2 = Zumbi()
zumbi3 = Zumbi()
zumbi4 = Zumbi()
zumbi5 = Zumbi()
lista_zumbis = []
lista_zumbis_0 = [zumbi0]
lista_zumbis_1 = [zumbi0, zumbi1, zumbi2]
lista_zumbis_2 = [zumbi0, zumbi1, zumbi2, zumbi3, zumbi4, zumbi5]


while True:
    relogio.tick(60)
    tela.fill((0,0,0))

    #Criação da mira no centro do mouse:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mira_rect.centerx = mouse_x
    mira_rect.centery = mouse_y
    tela.blit(imagem_mira, mira_rect)

    quantidade_abates_text = f'Abates: {quantidade_abates}'
    quantidade_abates_display = fonte.render(quantidade_abates_text, False, (255, 0, 0))
    tela.blit(quantidade_abates_display, (10, 10))
    display_vida = fonte.render(f'{jogador.vida}', False, (255, 0, 0))
    tela.blit(display_vida, (415, 10))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mira_x, mira_y = pygame.mouse.get_pos()
                distancia_x = mira_x - (jogador.posição_x + jogador.tamanho/2)
                distancia_y = mira_y - (jogador.posição_y + jogador.tamanho/2)
                distancia_total = max(1, abs(distancia_x) + abs(distancia_y))
                vetor_x = distancia_x / distancia_total
                vetor_y = distancia_y / distancia_total
                novo_projetil = Projetil(jogador, vetor_x, vetor_y)
                lista_projeteis.append(novo_projetil)
    jogador.movimentação_jogador(largura_tela, altura_tela)
    if quantidade_abates == 0:
        lista_zumbis = lista_zumbis_0
    elif quantidade_abates>0 and quantidade_abates<6:
        lista_zumbis = lista_zumbis_1
    elif quantidade_abates>5:
        lista_zumbis = lista_zumbis_2
    
    for indice_zumbi in range(0, len(lista_zumbis)):
        lista_zumbis[indice_zumbi].movimentação_zumbi(jogador)
        if lista_zumbis[indice_zumbi].hit_box.colliderect(jogador.hit_box):
            jogador.recebeu_mordida()
            if jogador.vida == 0:
                vitoria = False
                break
    copia_lista_projetil = lista_projeteis.copy()
    for projetil in copia_lista_projetil:
        projetil.movimentação_projetil()
        copia_lista_zumbi = lista_zumbis.copy()
        for zumbi in copia_lista_zumbi:
            if projetil.hit_box.colliderect(zumbi.hit_box) and projetil in lista_projeteis:
                lista_projeteis.remove(projetil)
                zumbi.recebeu_tiro()
            if zumbi.vida == 0:
                zumbi.posição_x, zumbi.posição_y = zumbi.coordenada_spawn_zumbi(largura_tela, altura_tela)
                zumbi.vida = 3
                quantidade_abates += 1

    pygame.display.update()
