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

#Configurações do Fundo:ssss
imagem_mapa = pygame.image.load('background.png').convert()
imagem_mapa = pygame.transform.scale(imagem_mapa, (800, 600))

#Configurações da Mira:
pygame.mouse.set_visible(False)
imagem_mira = pygame.image.load('mira.png').convert_alpha()
imagem_mira = pygame.transform.scale(imagem_mira, (40, 40))
mira_rect = imagem_mira.get_rect()

#Configurações do Marcador de Vida:
dicionario_coração = {}
for n in range(4):
    imagem_coração = pygame.image.load(f'coração/sprite_{n}.png').convert_alpha()
    imagem_coração = pygame.transform.scale(imagem_coração, (150, 50))
    dicionario_coração[n] = imagem_coração

#Configuração do Marcador de Munição:
dicionario_cooldown = {}
tempo_cooldown_sprite = 0.25
tempo_cooldown = 0.0
indice_cooldown = 0
for n in range(8):
    x = n
    y = 0
    if n>3:
        y = 1
        x -= 4
    imagem_cooldown = pygame.image.load(f'cooldown_sprite_sheet.png').subsurface((750*x,750*y),(750,750)).convert_alpha()
    imagem_cooldown = pygame.transform.scale(imagem_cooldown, (50, 50))
    dicionario_cooldown[n] = imagem_cooldown
imagem_arma_background = pygame.image.load('fundo_arma.png').convert_alpha()
imagem_arma_background = pygame.transform.scale(imagem_arma_background, (180, 62))
#(1444, 500)
imagem_beretta = pygame.image.load('beretta.png').convert_alpha()
imagem_beretta = pygame.transform.scale(imagem_beretta, (53, 36))
#(212, 144)

#Configurações do Marcador do Round:
dicionario_rounds = {}
for n in range(1, 6):
    imagem_round = pygame.image.load(f'rounds/round_{n}.png').convert_alpha()
    imagem_round = pygame.transform.scale(imagem_round, (100, 100))
    dicionario_rounds[n] = imagem_round

fonte = pygame.font.SysFont('impact', 35, False, True)
numero_round = 1
quantidade_abates = 0

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
grupo_zumbis_1 = pygame.sprite.Group()
grupo_zumbis_2 = pygame.sprite.Group()
grupo_zumbis_3 = pygame.sprite.Group()
grupo_zumbis_4 = pygame.sprite.Group()
grupo_zumbis_5 = pygame.sprite.Group()
for n in range(10):
    if n==9:
        zumbi_final = Zumbi(65,12)
        grupo_zumbis_5.add(zumbi_final)
    else:
        zumbi = Zumbi()
    if n<3:
        grupo_zumbis_1.add(zumbi)
    if n<5:
        grupo_zumbis_2.add(zumbi)
    if n<7:
        grupo_zumbis_3.add(zumbi)
    if n<9:
        grupo_zumbis_4.add(zumbi)
        grupo_zumbis_5.add(zumbi)
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
    delta_time = relogio.get_time()/1000
    tempo_atual = pygame.time.get_ticks()/1000

    #Definição da taxa de quadros por segundo:
    relogio.tick(60)

    #
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    tela.fill((0,0,0))
    tela.blit(imagem_mapa, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and jogador.munição>0:
                jogador.disparo(mouse_x, mouse_y, grupo_projeteis, Projetil)
        elif event.type == pygame.KEYDOWN:
            if event.key == K_r and jogador.munição<jogador.munição_total and jogador.tempo_recarga==0.0:
                jogador.recarga(delta_time)

    if jogador.munição == 0:
        recarga_completa = jogador.recarga(delta_time)
        if recarga_completa==False:
            if tempo_cooldown < tempo_cooldown_sprite:
                    tempo_cooldown += delta_time
            else:
                indice_cooldown += 1
                if indice_cooldown >= len(dicionario_cooldown):
                    indice_cooldown = 0
                tempo_cooldown = 0.0
        else:
            indice_cooldown = 0
            tempo_cooldown = 0.0
    jogador.movimentação_jogador(largura_tela, altura_tela, grupo_zumbis[numero_round], grupo_obstaculo, mouse_x, mouse_y)
    
    for zumbi in grupo_zumbis[numero_round]:
        zumbi.movimentação_zumbi(jogador, grupo_zumbis[numero_round], grupo_obstaculo, tempo_atual)
        if jogador.vida <= 0:
            running = False
            break

    for projetil in grupo_projeteis:
        projetil.movimentação_projetil(grupo_zumbis[numero_round], grupo_obstaculo)
    lista_zumbis_mortos = []
    for zumbi in grupo_zumbis[numero_round]:
        if zumbi.vida <= 0:
            lista_zumbis_mortos.append(zumbi)
            quantidade_abates += 1
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

    #Criação do display de vidas:
    tela.blit(dicionario_coração[jogador.vida], (10, 10))

    quantidade_abates_text = fonte.render(f'Abates: {quantidade_abates}', True, (255, 0, 0))
    tela.blit(quantidade_abates_text, (330, 10))

    #Criação do display de Rounds:
    tela.blit(dicionario_rounds[numero_round], (700, 10))

    #Criação do display de munição:
    tela.blit(imagem_arma_background, (670, 545))
    if jogador.munição==0:
        tela.blit(dicionario_cooldown[int(indice_cooldown)], (745, 545))
    else:
        numero_munição_text = fonte.render(f'{jogador.munição}', True, (255, 255, 255))
        tela.blit(numero_munição_text, (752, 550))
    tela.blit(imagem_beretta, (690, 554))

    #Criação da mira no centro do mouse:
    mira_rect.centerx = mouse_x
    mira_rect.centery = mouse_y
    tela.blit(imagem_mira, mira_rect)

    pygame.display.flip()
pygame.quit()