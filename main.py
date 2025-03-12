import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Antonio Recio: El Imperio del Marisco")

# Colores
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Cargar fondo estilo Inazuma Eleven
background = pygame.image.load("fondo.png")  # Asegúrate de tener un fondo adecuado
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Cargar sprite del personaje
antonio_img = pygame.image.load("antonio.png")  # Imagen de Antonio Recio
antonio_img = pygame.transform.scale(antonio_img, (50, 50))

# Posición inicial del personaje
antonio_x, antonio_y = WIDTH // 2, HEIGHT // 2
speed = 5

# Enemigos en el mapa
enemigos = [
    pygame.Rect(200, 150, 50, 50),
    pygame.Rect(500, 300, 50, 50),
    pygame.Rect(700, 450, 50, 50)
]

# Estados del juego
game_over = False
combate = False
enemigo_actual = None

# Reloj
clock = pygame.time.Clock()

running = True
while running:
    screen.blit(background, (0, 0))  # Dibujar fondo

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        antonio_x -= speed
    if keys[pygame.K_RIGHT]:
        antonio_x += speed
    if keys[pygame.K_UP]:
        antonio_y -= speed
    if keys[pygame.K_DOWN]:
        antonio_y += speed

    # Mantener a Antonio dentro de la pantalla
    antonio_x = max(0, min(WIDTH - 50, antonio_x))
    antonio_y = max(0, min(HEIGHT - 50, antonio_y))

    # Dibujar personaje
    screen.blit(antonio_img, (antonio_x, antonio_y))

    # Dibujar enemigos
    for enemigo in enemigos:
        pygame.draw.rect(screen, RED, enemigo)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
