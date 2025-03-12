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
background = pygame.image.load("static/images.jpeg")  # Asegúrate de tener un fondo adecuado
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_enrique = pygame.image.load("static/images.jpeg")  # Fondo casa de Enrique
background_enrique = pygame.transform.scale(background_enrique, (WIDTH, HEIGHT))
background_viejas = pygame.image.load("static/images.jpeg")  # Fondo casa de las viejas
background_viejas = pygame.transform.scale(background_viejas, (WIDTH, HEIGHT))

# Cargar sprite del personaje
antonio_img = pygame.image.load("static/recio.png")  # Imagen de Antonio Recio
antonio_img = pygame.transform.scale(antonio_img, (50, 50))

# Posición inicial del personaje
antonio_x, antonio_y = WIDTH // 2, HEIGHT // 2
speed = 5

# Escenarios y puertas
casas = {
    "Enrique": pygame.Rect(100, 100, 80, 80),  # Casa de Enrique (sin cambios)
    "Viejas": pygame.Rect(600, 350, 80, 80),   # Casa de las Viejas más baja
}

# Estados del juego
game_over = False
cinematica = None
dentro_casa = None

# Fuentes
font = pygame.font.Font(None, 36)

# Reloj
clock = pygame.time.Clock()

running = True
while running:
    if dentro_casa == "Enrique":
        screen.blit(background_enrique, (0, 0))
    elif dentro_casa == "Viejas":
        screen.blit(background_viejas, (0, 0))
    else:
        screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            dentro_casa = None  # Salir de la casa

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

    if dentro_casa is None:
        # Dibujar casas
        for nombre, casa in casas.items():
            pygame.draw.rect(screen, BLUE, casa)

        # Verificar colisiones con puertas
        for nombre, casa in casas.items():
            if pygame.Rect(antonio_x, antonio_y, 50, 50).colliderect(casa):
                cinematica = f"Antonio entra en la casa de {nombre}..."
                dentro_casa = nombre

    # Mostrar cinemática
    if cinematica:
        texto = font.render(cinematica, True, BLACK)
        screen.blit(texto, (50, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        cinematica = None

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
