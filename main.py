import pygame
from random import randint 
from random import Random
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
posiicao_Y = 520
velocidade = 1

pos_inimigo_x = 430
pos_inimigo_y = 50
velocidade_inimigo = 5

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    comando = pygame.key.get_pressed()

    if comando[pygame.K_UP or pygame.K_w]:
        posiicao_Y -= velocidade

    if comando[pygame.K_LEFT or pygame.K_a]:
        posicao_X -= velocidade

    if comando[pygame.K_DOWN or pygame.K_s]:
        posiicao_Y += velocidade

    if comando[pygame.K_RIGHT or pygame.K_d or pygame.K_d]:
        posicao_X += velocidade

    # Preencher a tela com a Imagem de fundo
    tela.blit(background_Game, (0,0))

    # Nave do Player
    tela.blit(player, (posicao_X, posiicao_Y))

    tela.blit(inimigo, (580,40))
    tela.blit(inimigo, (480,100))
    tela.blit(inimigo, (380,40))

    # Atualizar a tela
    pygame.display.update()

