import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Antonio Recio: Rey de las Gambas")

# Colores
WHITE = (255, 255, 255)
RED = (200, 0, 0)

# Cargar imágenes
antonio_img = pygame.image.load("recio.png")  # Reemplazar con una imagen válida
gamba_img = pygame.image.load("gamba.png")
obstaculo_img = pygame.image.load("recio.png")

# Escalar imágenes
gamba_img = pygame.transform.scale(gamba_img, (50, 50))
obstaculo_img = pygame.transform.scale(obstaculo_img, (50, 50))

# Jugador
player = pygame.Rect(WIDTH // 2, HEIGHT - 100, 60, 60)
player_speed = 5

# Lista de gambas y obstáculos
gambas = []
obstaculos = []

# Puntuación
score = 0
font = pygame.font.Font(None, 36)

# Reloj
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
        player.x += player_speed

    # Generar gambas y obstáculos aleatoriamente
    if random.randint(1, 50) == 1:
        gambas.append(pygame.Rect(random.randint(0, WIDTH - 50), 0, 50, 50))
    if random.randint(1, 80) == 1:
        obstaculos.append(pygame.Rect(random.randint(0, WIDTH - 50), 0, 50, 50))

    # Mover gambas y obstáculos
    for gamba in gambas[:]:
        gamba.y += 5
        if gamba.colliderect(player):
            score += 1
            gambas.remove(gamba)
        elif gamba.y > HEIGHT:
            gambas.remove(gamba)

    for obstaculo in obstaculos[:]:
        obstaculo.y += 5
        if obstaculo.colliderect(player):
            running = False  # Fin del juego si toca obstáculo
        elif obstaculo.y > HEIGHT:
            obstaculos.remove(obstaculo)

    # Dibujar elementos
    screen.blit(antonio_img, (player.x, player.y))
    for gamba in gambas:
        screen.blit(gamba_img, (gamba.x, gamba.y))
    for obstaculo in obstaculos:
        screen.blit(obstaculo_img, (obstaculo.x, obstaculo.y))

    # Mostrar puntuación
    score_text = font.render(f"Puntuación: {score}", True, RED)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

