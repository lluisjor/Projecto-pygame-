import pygame
import time

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trailer de Pygame")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fuentes
font = pygame.font.SysFont("Arial", 50)

# Cargar imágenes y sonidos (asegúrate de tener las rutas correctas)
background = pygame.image.load("static/lqsa2.png")
soundtrack = pygame.mixer.Sound("static/lqsa.mp3")


# Función para mostrar texto en pantalla
def display_text(text, color, y_offset):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)


# Reproducir música de fondo
pygame.mixer.Sound.play(soundtrack, loops=-1, maxtime=5000)  # Música en loop

# Loop principal
running = True
clock = pygame.time.Clock()

# Mostrar trailer
start_time = time.time()
while running:
    screen.fill(WHITE)

    # Fondo
    screen.blit(background, (0, 0))

    # Mostrar texto animado
    elapsed_time = time.time() - start_time
    if elapsed_time < 1:
        display_text("Bienvenidos al trailer", RED, -100)
    elif 1 <= elapsed_time < 3:
        display_text("¡Acción!", RED, -100)
    elif 3 <= elapsed_time < 5:
        display_text("Drama y emoción", RED, -100)
    elif 5 <= elapsed_time < 7:
        display_text("La aventura comienza", RED, -100)
    elif 7 <= elapsed_time < 10:
        display_text("Próximamente...", RED, -100)

    # Detectar eventos (como cerrar la ventana)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(30)  # Limitar a 30 FPS

pygame.quit()
