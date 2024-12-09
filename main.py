import pygame
from random import randint
import sys

# Inicializa o Pygame
pygame.init()

pygame.display.set_caption("Meu Jogo 2D")

LARGURA, ALTURA = 1080, 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
background_Game = pygame.image.load('Space-Game/Imagens/Background.jpg')
player = pygame.image.load('Space-Game/Imagens/Player.png')
inimigo = pygame.image.load('Space-Game/Imagens/Inimigo.png')
missil = pygame.image.load('Space-Game/Imagens/Missil.png')
explosão = pygame.image.load('Space-Game/Imagens/Explosao.png')

# Configuração inicial
posicao_X = 480
posicao_Y = 520
velocidade = 5

missil_Velocidade = 10

# Posições do inimigo
pos_inimigo_x = randint(0, LARGURA - inimigo.get_width())
pos_inimigo_y = randint(0, ALTURA // 2)
velocidade_inimigo_x = randint(-5, 5)
velocidade_inimigo_y = randint(-5, 5)

# Lista de mísseis disparados
misseis = []

# Relógio do jogo
relogio = pygame.time.Clock()

# Variáveis de estado do inimigo
inimigo_atingido = False  # Flag para indicar se o inimigo foi atingido
explosao_posicao = (0, 0)  # Posição da explosão
tempo_explosao = 0  # Tempo para controlar a duração da explosão

# Função para exibir a tela "Você perdeu"
def tela_voce_perdeu():
    fonte = pygame.font.SysFont("Arial", 72, bold=True)
    texto = fonte.render("Você perdeu!", True, (255, 0, 0))
    texto_rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2 - 50))

    fonte_botao = pygame.font.SysFont("Arial", 36)
    texto_botao = fonte_botao.render("Fechar", True, (255, 255, 255))
    botao_rect = pygame.Rect(LARGURA // 2 - 100, ALTURA // 2 + 50, 200, 50)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Clique esquerdo
                if botao_rect.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        tela.fill((0, 0, 0))  # Tela preta
        tela.blit(texto, texto_rect)

        # Desenhar o botão
        pygame.draw.rect(tela, (255, 0, 0), botao_rect)  # Retângulo do botão
        tela.blit(texto_botao, (botao_rect.x + 50, botao_rect.y + 10))  # Texto no botão

        pygame.display.update()
        relogio.tick(60)

# Loop principal do jogo
tempo_para_meteoro = 0
misseis_disparados = False  # Flag para garantir que apenas um míssil seja disparado

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

    # Disparar o míssil apenas uma vez ao pressionar espaço
    if comando[pygame.K_SPACE] and not misseis_disparados:  
        misseis.append(pygame.Rect(posicao_X + player.get_width() // 2 - missil.get_width() // 2, posicao_Y, missil.get_width(), missil.get_height()))
        misseis_disparados = True  # Marcar que um míssil foi disparado

    # Se a tecla espaço não estiver mais pressionada, permitir disparar novamente
    if not comando[pygame.K_SPACE]:
        misseis_disparados = False

    # Impedir que o jogador saia da tela
    posicao_X = max(0, min(LARGURA - player.get_width(), posicao_X))
    posicao_Y = max(0, min(ALTURA - player.get_height(), posicao_Y))

    # Atualizar posição do inimigo, se ainda não for atingido
    if not inimigo_atingido:
        pos_inimigo_x += velocidade_inimigo_x
        pos_inimigo_y += velocidade_inimigo_y

    # Verificar colisão com bordas da tela
    if pos_inimigo_x <= 0 or pos_inimigo_x >= LARGURA - inimigo.get_width():
        velocidade_inimigo_x *= -1
    if pos_inimigo_y <= 0 or pos_inimigo_y >= ALTURA // 2 - inimigo.get_height():
        velocidade_inimigo_y *= -1

    # Alterar direção aleatoriamente em intervalos de tempo
    tempo_para_meteoro += 1
    if tempo_para_meteoro > 30:
        velocidade_inimigo_x = randint(-5, 5)
        velocidade_inimigo_y = randint(-5, 5)
        tempo_para_meteoro = 0

    # Criação de retângulos
    rect_player = pygame.Rect(posicao_X, posicao_Y, player.get_width(), player.get_height())
    rect_inimigo = pygame.Rect(pos_inimigo_x, pos_inimigo_y, inimigo.get_width(), inimigo.get_height())

    # Verificar colisão do míssil com o inimigo
    for missil_rect in misseis[:]:
        missil_rect.y -= missil_Velocidade  # Mover o míssil para cima

        # Verificar se o míssil saiu da tela
        if missil_rect.y < 0:
            misseis.remove(missil_rect)
        else:
            tela.blit(missil, missil_rect)

        # Verificar colisão do míssil com o inimigo
        if missil_rect.colliderect(rect_inimigo) and not inimigo_atingido:
            misseis.remove(missil_rect)
            # Marcar que o inimigo foi atingido e a explosão deve ocorrer
            inimigo_atingido = True
            explosao_posicao = (pos_inimigo_x, pos_inimigo_y)  # Armazenar a posição para a explosão
            tempo_explosao = pygame.time.get_ticks()  # Armazenar o tempo atual para controlar a duração da explosão

    # Desenhar o fundo
    tela.blit(background_Game, (0, 0))

    # Nave do Player
    tela.blit(player, (posicao_X, posicao_Y))

    # Desenhar inimigo ou explosão dependendo da colisão
    if inimigo_atingido:
        # Mostrar a explosão por 1 segundo
        if pygame.time.get_ticks() - tempo_explosao < 1000:
            tela.blit(explosão, explosao_posicao)  # Mostrar a explosão
        else:
            # Após 1 segundo, o inimigo perde a colisão e a explosão desaparece
            inimigo_atingido = False
            pos_inimigo_x = randint(0, LARGURA - inimigo.get_width())  # Reposicionar o inimigo
            pos_inimigo_y = randint(0, ALTURA // 2)  # Reposicionar o inimigo
    else:
        tela.blit(inimigo, (pos_inimigo_x, pos_inimigo_y))  # Caso contrário, desenhar o inimigo

    # Mover e desenhar os mísseis
    for missil_rect in misseis[:]:
        missil_rect.y -= missil_Velocidade  # Mover o míssil para cima

        # Verificar se o míssil saiu da tela
        if missil_rect.y < 0:
            misseis.remove(missil_rect)
        else:
            tela.blit(missil, missil_rect)

    # Atualizar a tela
    pygame.display.update()
    relogio.tick(60)