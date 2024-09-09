import pygame
import sys

# Inicializando o pygame
pygame.init()

# Definindo constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
BALL_SPEED_X, BALL_SPEED_Y = 4, 4
PADDLE_SPEED = 6
OPPONENT_SPEED = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Criando a janela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Definindo as posições e dimensões
# Bola menor e quadrada
ball = pygame.Rect(SCREEN_WIDTH / 2 - 10, SCREEN_HEIGHT / 2 - 10, 20, 20)

# Raquetes maiores e mais largas, como na imagem
player = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT / 2 - 50, 10, 100)
opponent = pygame.Rect(10, SCREEN_HEIGHT / 2 - 50, 10, 100)

# Velocidades iniciais da bola e dos jogadores
ball_speed_x, ball_speed_y = BALL_SPEED_X, BALL_SPEED_Y
player_speed, opponent_speed = 0, OPPONENT_SPEED

# Pontuações dos jogadores
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

# Função para desenhar os objetos na tela
def draw():
    screen.fill(BLACK)
    
    # Desenhando as raquetes
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, opponent)
    
    # Desenhando a bola quadrada
    pygame.draw.rect(screen, WHITE, ball)
    
    # Desenhando a linha pontilhada no meio
    for i in range(0, SCREEN_HEIGHT, 20):
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH / 2 - 2, i, 4, 10))
    
    # Exibir pontuação
    player_text = font.render(f"{player_score}", True, WHITE)
    screen.blit(player_text, (SCREEN_WIDTH / 2 + 20, 20))

    opponent_text = font.render(f"{opponent_score}", True, WHITE)
    screen.blit(opponent_text, (SCREEN_WIDTH / 2 - 40, 20))

# Atualizando a posição da bola
def update_ball():
    global ball_speed_x, ball_speed_y, player_score, opponent_score

    # Movimentando a bola
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Colisão com as paredes superiores/inferiores
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    # Colisão com os jogadores
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

    # Verificar se a bola passou da raquete do jogador ou do oponente
    if ball.left <= 0:  # Oponente errou
        player_score += 1
        reset_ball()

    if ball.right >= SCREEN_WIDTH:  # Jogador errou
        opponent_score += 1
        reset_ball()

# Função para resetar a bola no centro
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    ball_speed_x *= -1  # Inverter a direção da bola após pontuação

# Movendo o oponente com previsão
def update_opponent():
    if ball_speed_x < 0:  # Apenas mover se a bola estiver se aproximando
        # Se a bola estiver acima do centro da raquete do oponente
        if opponent.centery < ball.centery:
            opponent.y += OPPONENT_SPEED
        # Se a bola estiver abaixo do centro da raquete do oponente
        elif opponent.centery > ball.centery:
            opponent.y -= OPPONENT_SPEED

        # Adiciona uma área de tolerância para não ajustar de maneira muito precisa
        if abs(opponent.centery - ball.centery) < 30:
            opponent_speed = 0
        else:
            opponent_speed = OPPONENT_SPEED

    # Impedir que o oponente saia da tela
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT

# Função principal
def main():
    global player_speed

    clock = pygame.time.Clock()

    while True:
        # Tratando eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_speed = PADDLE_SPEED
                if event.key == pygame.K_UP:
                    player_speed = -PADDLE_SPEED

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    player_speed = 0

        # Atualizando a posição dos jogadores
        player.y += player_speed

        # Mantendo os jogadores na tela
        if player.top <= 0:
            player.top = 0
        if player.bottom >= SCREEN_HEIGHT:
            player.bottom = SCREEN_HEIGHT

        # Chamando as funções de atualização
        update_ball()
        update_opponent()

        # Desenhando os objetos
        draw()

        # Atualizando a tela
        pygame.display.flip()

        # Limitando a taxa de quadros
        clock.tick(60)

if __name__ == '__main__':
    main()
