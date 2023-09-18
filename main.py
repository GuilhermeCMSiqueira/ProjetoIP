import pygame
import sys
import random
import math
import time

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo de Sobrevivente")

relogio = pygame.time.Clock()

# Cores
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
preto = (0, 0, 0)

# Importando as classes
from classes import Sobrevivente
from classes import Zumbi
from classes import Projetil

# Criar o objeto Sobrevivente
sobrevivente = Sobrevivente()

# Criar zumbis
num_zumbis = 5  # Número de zumbis
zumbis = Zumbi.criar_zumbis(num_zumbis)

# Variáveis dos contadores
contagem_azul = 0
contagem_verde = 0
contagem_vermelho = 0
contagem_mortes = 0

# Conjunto para rastrear zumbis que já colidiram
zumbis_colididos = set()

tempo_inicial = 60  # Tempo inicial em segundos
tempo_decorrido = 0  # Tempo decorrido em segundos
tempo_ultimo_quadro = time.time()

# Função para mostrar mensagem
def mostrar_mensagem(mensagem, duracao):
    fonte = pygame.font.Font(None, 72)
    texto = fonte.render(mensagem, True, vermelho)
    tela.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2 - texto.get_height() // 2))
    pygame.display.update()
    time.sleep(duracao)  # Aguarde por alguns segundos

# Loop principal do jogo
while True:
    relogio.tick(120)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Botão esquerdo do mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()
                sobrevivente.atirar(mouse_x, mouse_y)

    for projetil in sobrevivente.projeteis:
        for zumbi in zumbis:
            if (
                projetil.x < zumbi.x + zumbi.tamanho and
                projetil.x + Projetil.tamanho_projetil > zumbi.x and
                projetil.y < zumbi.y + zumbi.tamanho and
                projetil.y + Projetil.tamanho_projetil > zumbi.y
            ):
                # O projétil atingiu o zumbi
                if zumbi.tipo == "azul":
                    contagem_azul += 1
                elif zumbi.tipo == "verde":
                    contagem_verde += 1
                elif zumbi.tipo == "vermelho":
                    contagem_vermelho += 1

                zumbi.vida -= 1
                if zumbi.vida <= 0:
                    # Remova o zumbi da lista
                    zumbis.remove(zumbi)
                    # Crie um novo zumbi fora da tela com a mesma velocidade
                    novo_zumbi = Zumbi(random.choice(["azul", "verde", "vermelho"]), random.randint(40, 40), zumbi.velocidade)
                    zumbis.append(novo_zumbi)
                # Remova o projétil da lista

    for zumbi in zumbis:
        if (
            sobrevivente.x < zumbi.x + zumbi.tamanho and
            sobrevivente.x + sobrevivente.tamanho > zumbi.x and
            sobrevivente.y < zumbi.y + zumbi.tamanho and
            sobrevivente.y + sobrevivente.tamanho > zumbi.y
        ):
            # O zumbi colidiu com o sobrevivente
            if zumbi not in zumbis_colididos:  # Verifique se o zumbi não colidiu anteriormente
                contagem_mortes += 1
                zumbis_colididos.add(zumbi)  # Adicione o zumbi ao conjunto de colisões

    # Verifica as teclas pressionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a]:
        sobrevivente.mover("esquerda")
    if teclas[pygame.K_d]:
        sobrevivente.mover("direita")
    if teclas[pygame.K_w]:
        sobrevivente.mover("cima")
    if teclas[pygame.K_s]:
        sobrevivente.mover("baixo")

    # Atualiza a posição dos zumbis seguindo o sobrevivente
    for zumbi in zumbis:
        zumbi.seguir_sobrevivente(sobrevivente)

    # Atualiza a posição dos projéteis e remove-os quando saem da tela
    sobrevivente.projeteis = [projetil for projetil in sobrevivente.projeteis if projetil.y > 0]
    for projetil in sobrevivente.projeteis:
        projetil.mover()

    # Calcula o tempo decorrido desde o último quadro
    tempo_atual = time.time()
    delta_tempo = tempo_atual - tempo_ultimo_quadro
    tempo_ultimo_quadro = tempo_atual

    # Atualiza o tempo decorrido
    tempo_decorrido += delta_tempo

    # Verifique as condições de derrota e vitória
    if contagem_mortes >= 3:
        # Condição de derrota
        mostrar_mensagem("Você perdeu!", 0.5)
        pygame.quit()
        sys.exit()
   
    if tempo_decorrido >= tempo_inicial and contagem_mortes < 3:
        # Condição de vitória
        mostrar_mensagem("Você venceu!", 0.5)
        pygame.quit()
        sys.exit()

    # Limpa a tela
    tela.fill(branco)

    # Desenha o Sobrevivente
    sobrevivente.desenhar()

    # Desenha os Zumbis
    for zumbi in zumbis:
        zumbi.desenhar()

    # Desenha os Projéteis
    for projetil in sobrevivente.projeteis:
        projetil.desenhar()

    # Desenha os contadores na parte superior da tela
    fonte = pygame.font.Font(None, 26)
    texto_azul = fonte.render(f'Azul: {contagem_azul}', True, azul)
    texto_verde = fonte.render(f'Verde: {contagem_verde}', True, verde)
    texto_vermelho = fonte.render(f'Vermelho: {contagem_vermelho}', True, vermelho)
    texto_mortes = fonte.render(f'Mortes: {contagem_mortes}', True, preto)
    texto_tempo = fonte.render(f'Tempo: {int(tempo_inicial - tempo_decorrido)}', True, preto)

    tela.blit(texto_azul, (240, 10))
    tela.blit(texto_verde, (330, 10))
    tela.blit(texto_vermelho, (420, 10))
    tela.blit(texto_mortes, (290, 50))
    tela.blit(texto_tempo, (380, 50))

    # Atualiza a tela
    pygame.display.update()
