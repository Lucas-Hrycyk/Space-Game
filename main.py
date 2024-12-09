import pygame
from random import randint, choice
import sys

# Inicializa o Pygame
pygame.init()

pygame.display.set_caption("Meu Jogo 2D")

LARGURA, ALTURA = 1080, 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
background_Game = pygame.image.load('Space-Game/Imagens/Background.jpg')
player = pygame.image.load('Space-Game/Imagens/Player.png')
inimigo = pygame.image.load('Space-Game/Imagens/Inimigo.png')

posicao_X = 480
posicao_Y = 520
velocidade = 5

pos_inimigo_x = randint(0, LARGURA - inimigo.get_width())
pos_inimigo_y = randint(0, ALTURA // 2)
velocidade_inimigo_x = randint(-5, 5)
velocidade_inimigo_y = randint(-5, 5)

relogio = pygame.time.Clock()
mudanca_tempo = 0

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    comando = pygame.key.get_pressed()

    if comando[pygame.K_UP] or comando[pygame.K_w]:
        posicao_Y -= velocidade
    if comando[pygame.K_LEFT] or comando[pygame.K_a]:
        posicao_X -= velocidade
    if comando[pygame.K_DOWN] or comando[pygame.K_s]:
        posicao_Y += velocidade
    if comando[pygame.K_RIGHT] or comando[pygame.K_d]:
        posicao_X += velocidade

    # Atualizar posição do inimigo
    pos_inimigo_x += velocidade_inimigo_x
    pos_inimigo_y += velocidade_inimigo_y

    # Verificar colisão com bordas da tela
    if pos_inimigo_x <= 0 or pos_inimigo_x >= LARGURA - inimigo.get_width():
        velocidade_inimigo_x *= -1
    if pos_inimigo_y <= 0 or pos_inimigo_y >= ALTURA // 2 - inimigo.get_height():
        velocidade_inimigo_y *= -1

    # Alterar direção aleatoriamente em intervalos de tempo
    mudanca_tempo += 1
    if mudanca_tempo > 30:  # Muda de direção a cada 30 quadros (~0.5 segundos)
        velocidade_inimigo_x = randint(-5, 5)
        velocidade_inimigo_y = randint(-5, 5)
        mudanca_tempo = 0

    # Preencher a tela com a Imagem de fundo
    tela.blit(background_Game, (0, 0))

    # Nave do Player
    tela.blit(player, (posicao_X, posicao_Y))

    # Nave Inimiga
    tela.blit(inimigo, (pos_inimigo_x, pos_inimigo_y))

    # Atualizar a tela
    pygame.display.update()
    relogio.tick(60)