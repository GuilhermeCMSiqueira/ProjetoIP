import pygame
from pygame.locals import *
from sys import exit
from Jogador import Jogador
from Projetil import Projetil
from Zumbi import Zumbi
from KitMedico import KitMedico
from Obstaculo import Obstaculo
from BombaNuclear import Bomba

pygame.init()

#Configurações da Janela:
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('CInZombie')

#Configurações do Fundo:
imagem_mapa = pygame.image.load('background.png').convert()
imagem_mapa = pygame.transform.scale(imagem_mapa, (800, 600))

#Configurações da Mira:
pygame.mouse.set_visible(False)
imagem_mira = pygame.image.load('mira.png').convert_alpha()
imagem_mira = pygame.transform.scale(imagem_mira, (40, 40))
mira_rect = imagem_mira.get_rect()

#Configurações do Marcador de Vida:
imagem_um_coração = pygame.image.load('coração/sprite_0.png').convert_alpha()
imagem_um_coração = pygame.transform.scale(imagem_um_coração, (150, 50))
imagem_dois_corações = pygame.image.load('coração/sprite_1.png').convert_alpha()
imagem_dois_corações = pygame.transform.scale(imagem_dois_corações, (150, 50))
imagem_três_corações = pygame.image.load('coração/sprite_2.png').convert_alpha()
imagem_três_corações = pygame.transform.scale(imagem_três_corações, (150, 50))

#Configuração do Marcador de Munição:
imagem_beretta = pygame.image.load('armas/beretta_9mm.png').convert_alpha()
imagem_beretta = pygame.transform.scale(imagem_beretta, (120, 60))

#Configurações do Marcador do Round:
imagem_round_um = pygame.image.load('rounds/round_1.png').convert_alpha()
imagem_round_um = pygame.transform.scale(imagem_round_um, (100, 100))
imagem_round_dois = pygame.image.load('rounds/round_2.png').convert_alpha()
imagem_round_dois = pygame.transform.scale(imagem_round_dois, (100, 100))
imagem_round_três = pygame.image.load('rounds/round_3.png').convert_alpha()
imagem_round_três = pygame.transform.scale(imagem_round_três, (100, 100))
imagem_round_quatro = pygame.image.load('rounds/round_4.png').convert_alpha()
imagem_round_quatro = pygame.transform.scale(imagem_round_quatro, (100, 100))
imagem_round_cinco = pygame.image.load('rounds/round_5.png').convert_alpha()
imagem_round_cinco = pygame.transform.scale(imagem_round_cinco, (100, 100))

fonte = pygame.font.SysFont('impact', 40, False, True)
numero_round = 1

relogio = pygame.time.Clock()
tempo_inicial = pygame.time.get_ticks()/1000

#Objetos e Grupo de Obstaculos:
carro = Obstaculo(515, 345, 120, 65)
grupo_obstaculo = pygame.sprite.Group()
grupo_obstaculo.add(carro)

#Objeto e Grupo do jogador:
jogador = Jogador(largura_tela, altura_tela)
grupo_jogador = pygame.sprite.Group()
grupo_jogador.add(jogador)

#Objetos e Grupos de zumbis:
zumbi1 = Zumbi()
zumbi2 = Zumbi()
zumbi3 = Zumbi()
zumbi4 = Zumbi()
zumbi5 = Zumbi()
zumbi6 = Zumbi()
zumbi7 = Zumbi()
zumbi8 = Zumbi()
Zumbi9 = Zumbi()
zumbi_final = Zumbi(60, 12)
grupo_zumbis_1 = pygame.sprite.Group()
grupo_zumbis_1.add(zumbi1, zumbi2, zumbi3)
grupo_zumbis_2 = pygame.sprite.Group()
grupo_zumbis_2.add(zumbi1, zumbi2, zumbi3, zumbi4, zumbi5)
grupo_zumbis_3 = pygame.sprite.Group()
grupo_zumbis_3.add(zumbi1, zumbi2, zumbi3, zumbi4, zumbi5, zumbi6, zumbi7)
grupo_zumbis_4 = pygame.sprite.Group()
grupo_zumbis_4.add(zumbi1, zumbi2, zumbi3, zumbi4, zumbi5, zumbi6, zumbi7, zumbi8, Zumbi9)
grupo_zumbis_5 = pygame.sprite.Group()
grupo_zumbis_5.add(zumbi1, zumbi2, zumbi3, zumbi4, zumbi5, zumbi6, zumbi7, zumbi8, Zumbi9, zumbi_final)
grupo_zumbis = {1:grupo_zumbis_1, 2:grupo_zumbis_2, 3:grupo_zumbis_3, 4:grupo_zumbis_4, 5:grupo_zumbis_5}

#Grupo dos projeteis:
grupo_projeteis = pygame.sprite.Group()

#Grupo dos kits médicos:
grupo_kitmedico = pygame.sprite.Group()

#Grupo da bomba nuclear:
grupo_bomba = pygame.sprite.Group()

running = True
while running==True:
    #Cálculo do Delta Time(tempo entre quadros):
    tempo_atual = pygame.time.get_ticks()/1000
    delta_time = tempo_atual - tempo_inicial
    tempo_inicial = tempo_atual

    #Definição da taxa de quadros por segundo:
    relogio.tick(60)


    tela.fill((0,0,0))
    tela.blit(imagem_mapa, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and jogador.munição>0:
                novo_projetil = Projetil(mouse_x, mouse_y, jogador, delta_time)
                grupo_projeteis.add(novo_projetil)
        elif event.type == pygame.KEYDOWN:
            if event.key == K_r and jogador.munição<jogador.munição_total and jogador.tempo_recarga==0.0:
                jogador.recarga(delta_time)

    if jogador.munição == 0:
        jogador.recarga(delta_time)
    jogador.movimentação_jogador(largura_tela, altura_tela, grupo_zumbis[numero_round], grupo_obstaculo)
    
    for zumbi in grupo_zumbis[numero_round]:
        zumbi.movimentação_zumbi(jogador, grupo_zumbis[numero_round], grupo_obstaculo, tempo_atual)
        if jogador.vida <= 0:
            running = False
            break

    for projetil in grupo_projeteis:
        projetil.movimentação_projetil(grupo_zumbis[numero_round])
    lista_zumbis_mortos = []
    for zumbi in grupo_zumbis[numero_round]:
        if zumbi.vida <= 0:
            lista_zumbis_mortos.append(zumbi)
    for zumbi in lista_zumbis_mortos:
        if zumbi!=zumbi_final and zumbi.drop_kit_medico() == True:
            kitmedico = KitMedico(zumbi)
            grupo_kitmedico.add(kitmedico)
        if zumbi == zumbi_final:
            bomba = Bomba(zumbi)
            grupo_bomba.add(bomba)
            grupo_zumbis[numero_round].remove(zumbi)
        elif numero_round == 5:
            zumbi.rect.x, zumbi.rect.y = zumbi.coordenada_spawn_zumbi(largura_tela, altura_tela)
        elif zumbi in grupo_zumbis[numero_round]:
            grupo_zumbis[numero_round].remove(zumbi)
    if len(grupo_zumbis[numero_round]) == 0:
        numero_round += 1
        for zumbi in grupo_zumbis[numero_round]:
            if zumbi != zumbi_final:
                zumbi.rect.x, zumbi.rect.y = zumbi.coordenada_spawn_zumbi(largura_tela, altura_tela)

    colisoes_bomba_jogador = pygame.sprite.groupcollide(grupo_bomba, grupo_jogador,True, False)
    for colisoes in colisoes_bomba_jogador:
        running = False
        break
    grupo_bomba.draw(tela)

    for sprite in grupo_kitmedico:
        sprite.temporizador()
    colisoes_kitmedico_jogador = pygame.sprite.groupcollide(grupo_kitmedico, grupo_jogador, True, False)
    for colisoes in colisoes_kitmedico_jogador:
        jogador.pegou_kitmedico()
    grupo_kitmedico.draw(tela)

    #Criação do display de Rounds:
    if numero_round == 1:
        imagem_contador_round = imagem_round_um
    elif numero_round == 2:
        imagem_contador_round = imagem_round_dois
    elif numero_round == 3:
        imagem_contador_round = imagem_round_três
    elif numero_round == 4:
        imagem_contador_round = imagem_round_quatro
    else:
        imagem_contador_round = imagem_round_cinco
    tela.blit(imagem_contador_round, (700, 10))

    #Criação do display de vidas:
    if jogador.vida == 3:
        imagem_contador_vida = imagem_três_corações
    elif jogador.vida == 2:
        imagem_contador_vida = imagem_dois_corações
    elif jogador.vida == 1:
        imagem_contador_vida = imagem_um_coração
    else:
        imagem_contador_vida = pygame.Surface((50, 50))
        imagem_contador_vida.fill((0,0,0,0))
    tela.blit(imagem_contador_vida, (10, 10))

    #Criação do display de munição:
    numero_munição_text = fonte.render(f'{jogador.munição}', True, (255, 0, 0))
    tela.blit(imagem_beretta, (700, 530))
    tela.blit(numero_munição_text, (680, 539))

    #Criação da mira no centro do mouse:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mira_rect.centerx = mouse_x
    mira_rect.centery = mouse_y
    tela.blit(imagem_mira, mira_rect)

    pygame.display.flip()
pygame.quit()
