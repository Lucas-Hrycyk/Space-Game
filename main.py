import pygame
from random import randint
import sys

# Inicializa o Pygame
pygame.init()

# Configurações básicas
LARGURA, ALTURA = 1080, 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu Jogo 2D")
relogio = pygame.time.Clock()

# Carregando imagens
background = pygame.image.load('Space-Game/Imagens/Background.jpg')
player_img = pygame.image.load('Space-Game/Imagens/Player.png')
inimigo_img = pygame.image.load('Space-Game/Imagens/Inimigo.png')
missil_img = pygame.image.load('Space-Game/Imagens/Missil.png')
missil_inimigo_img = pygame.image.load('Space-Game/Imagens/MissilInimigo.png')
explosao_img = pygame.image.load('Space-Game/Imagens/Explosao.png')

# Variáveis do jogador
player_x = 480
player_y = 520
player_vel = 5

# Variáveis dos inimigos
inimigos = []
inimigo_vel = 3

# Variáveis de pontuação
pontuacao = 0

# Listas de mísseis
misseis = []
misseis_inimigos = []
missil_vel = 10

# Tempo de reinício do inimigo com intervalo aleatório entre 1 e 3 inimigos a cada 5 segundos
tempo_para_novo_inimigo = 0
intervalo_inimigo = 5000

# Velocidade do fundo (movimento devagar)
velocidade_fundo = 2.5  

# Função para gerar um novo inimigo
def gerar_inimigo():
    if len(inimigos) < 10:
        inimigos_gerados = randint(1, 3)
        for _ in range(inimigos_gerados):
            inimigo_x = randint(0, LARGURA - inimigo_img.get_width())
            inimigo_y = randint(0, ALTURA // 2)
            inimigo_vel_x = randint(-5, 5)
            inimigo_vel_y = randint(-5, 5)
            inimigos.append({
                'x': inimigo_x,
                'y': inimigo_y,
                'vel_x': inimigo_vel_x,
                'vel_y': inimigo_vel_y,
                'img': inimigo_img,
                'missil_timer': 0 
            })

# Função para exibir a tela de derrota e pontuação final
def tela_voce_perdeu(pontos):
    fonte = pygame.font.SysFont("Arial", 72, bold=True)
    texto = fonte.render("Você perdeu!", True, (255, 0, 0))
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2 - 50))
    pontos_rect = texto_pontos.get_rect(center=(LARGURA // 2, ALTURA // 2 + 50))

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela.fill((0, 0, 0))
        tela.blit(texto, texto_rect)
        tela.blit(texto_pontos, pontos_rect)
        pygame.display.update()
        relogio.tick(60)

# Função para mostrar a explosão
def mostrar_explosao(x, y):
    tela.blit(explosao_img, (x, y))
    pygame.display.update()
    pygame.time.delay(200)  # Tempo para a explosão ser visível antes de desaparecer

# Função para mover o background automaticamente de forma lenta
def mover_background_lento():
    fundo_y = (pygame.time.get_ticks() // velocidade_fundo) % ALTURA
    tela.blit(background, (0, fundo_y - ALTURA))
    tela.blit(background, (0, fundo_y))

# Gerar um inimigo ao iniciar o jogo
gerar_inimigo()

# Loop principal do jogo
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Comandos do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        player_y -= player_vel
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        player_y += player_vel
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        player_x -= player_vel
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        player_x += player_vel

    # Disparo do jogador
    if teclas[pygame.K_SPACE]:
        if len(misseis) == 0:  # Permitir apenas um míssil por vez
            misseis.append(pygame.Rect(
                player_x + player_img.get_width() // 2 - missil_img.get_width() // 2,
                player_y, missil_img.get_width(), missil_img.get_height()
            ))

    # Restrições do jogador na tela
    player_x = max(0, min(LARGURA - player_img.get_width(), player_x))
    player_y = max(0, min(ALTURA - player_img.get_height(), player_y))

    # Movimento dos inimigos
    for inimigo in inimigos:
        inimigo['x'] += inimigo['vel_x']
        inimigo['y'] += inimigo['vel_y']

        # Limitar a velocidade máxima dos inimigos
        if abs(inimigo['vel_x']) > 5:
            inimigo['vel_x'] = 5 * (inimigo['vel_x'] / abs(inimigo['vel_x']))  # Normaliza para -5 ou 5
        if abs(inimigo['vel_y']) > 5:
            inimigo['vel_y'] = 5 * (inimigo['vel_y'] / abs(inimigo['vel_y']))  # Normaliza para -5 ou 5

        # Reversão de direção ao atingir a borda da tela
        if inimigo['x'] <= 0 or inimigo['x'] >= LARGURA - inimigo['img'].get_width():
            inimigo['vel_x'] = -inimigo['vel_x']  # Inverte a direção no eixo X
        if inimigo['y'] <= 0 or inimigo['y'] >= ALTURA // 2 - inimigo['img'].get_height():
            inimigo['vel_y'] = -inimigo['vel_y']  # Inverte a direção no eixo Y

        # Alteração de direção ocasional (diminui a chance para movimentos mais naturais)
        if randint(0, 100) < 2:  # 2% de chance de mudar a direção
            inimigo['vel_x'] = randint(-5, 5)
            inimigo['vel_y'] = randint(-5, 5)

        # Lógica para disparar mísseis de inimigos a cada 2 segundos
        inimigo['missil_timer'] += relogio.get_time()
        if inimigo['missil_timer'] >= 2000:  # Dispara a cada 2 segundos
            misseis_inimigos.append(pygame.Rect(
                inimigo['x'] + inimigo_img.get_width() // 2 - missil_inimigo_img.get_width() // 2,
                inimigo['y'] + inimigo_img.get_height(), missil_inimigo_img.get_width(), missil_inimigo_img.get_height()
            ))
            inimigo['missil_timer'] = 0  # Reinicia o temporizador

    # Movimento dos mísseis do jogador
    for missil_rect in misseis[:]:
        missil_rect.y -= missil_vel
        if missil_rect.y < 0:  # Remover mísseis que saem da tela
            misseis.remove(missil_rect)
        else:
            for inimigo in inimigos[:]:
                if missil_rect.colliderect(pygame.Rect(inimigo['x'], inimigo['y'], inimigo_img.get_width(), inimigo_img.get_height())):
                    misseis.remove(missil_rect)
                    inimigos.remove(inimigo)
                    pontuacao += 100  # Incrementar pontos ao acertar o inimigo
                    mostrar_explosao(inimigo['x'], inimigo['y'])
                    break

    # Movimento dos mísseis dos inimigos
    for missil_inimigo_rect in misseis_inimigos[:]:
        missil_inimigo_rect.y += missil_vel
        if missil_inimigo_rect.y > ALTURA:
            misseis_inimigos.remove(missil_inimigo_rect)
        elif missil_inimigo_rect.colliderect(pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())):
            tela_voce_perdeu(pontuacao)

    # Gerar novos inimigos a cada 5 segundos
    tempo_para_novo_inimigo += relogio.get_time()
    if tempo_para_novo_inimigo >= intervalo_inimigo:
        gerar_inimigo()
        tempo_para_novo_inimigo = 0

    # Desenho dos elementos
    mover_background_lento()  # Movimento lento do fundo
    tela.blit(player_img, (player_x, player_y))

    for inimigo in inimigos:
        tela.blit(inimigo['img'], (inimigo['x'], inimigo['y']))

    for missil_rect in misseis:
        tela.blit(missil_img, missil_rect)

    for missil_inimigo_rect in misseis_inimigos:
        tela.blit(missil_inimigo_img, missil_inimigo_rect)

    # Exibição da pontuação atual
    fonte = pygame.font.SysFont("Arial", 24)
    texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, (255, 255, 255))
    tela.blit(texto_pontos, (10, 10))

    pygame.display.update()
    relogio.tick(60)
