import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # Ajustado para mover el fondo
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 1200, 1157  # Tamaño del fondo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Antonio Recio: El Imperio del Marisco")

# Colores
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARK_RED = (139, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Cargar imágenes
fondo_inicio = pygame.image.load("static/fondo.png")
fondo_inicio = pygame.transform.scale(fondo_inicio, (SCREEN_WIDTH, SCREEN_HEIGHT))

background = pygame.image.load("static/lqsa1.png")
background = pygame.transform.scale(background, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

antonio_img = pygame.image.load("static/enrique.png")
antonio_img = pygame.transform.scale(antonio_img, (50, 50))

# Estados del juego
game_over = False
cinematica = None
dentro_casa = None

# Barra de vida
vida_maxima = 100
vida_actual = vida_maxima

# Reloj
clock = pygame.time.Clock()

# Posiciones iniciales
bg_x, bg_y = -(BACKGROUND_WIDTH - SCREEN_WIDTH) // 2, -(BACKGROUND_HEIGHT - SCREEN_HEIGHT) // 2
antonio_x, antonio_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Límites para mover el fondo
MARGIN_X, MARGIN_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
delta = 5  # Velocidad de movimiento

# Función para la pantalla de inicio
def pantalla_inicio():
    font = pygame.font.Font(None, 48)
    texto_jugar = font.render("Presiona ENTER para Jugar", True, WHITE)
    texto_salir = font.render("Presiona ESC para Salir", True, WHITE)

    screen.blit(fondo_inicio, (0, 0))
    screen.blit(texto_jugar, (SCREEN_WIDTH // 2 - texto_jugar.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
    screen.blit(texto_salir, (SCREEN_WIDTH // 2 - texto_salir.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

    pygame.display.flip()

# Función para dibujar la barra de vida
def dibujar_barra_vida():
    pygame.draw.rect(screen, DARK_RED, (10, 10, 300, 30))
    color_vida = GREEN if vida_actual > vida_maxima * 0.7 else YELLOW if vida_actual > vida_maxima * 0.3 else RED
    pygame.draw.rect(screen, color_vida, (10, 10, (vida_actual / vida_maxima) * 300, 30))

# Función para reiniciar el juego
def reiniciar_juego():
    global antonio_x, antonio_y, vida_actual, dentro_casa, cinematica, game_over, bg_x, bg_y
    antonio_x, antonio_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    bg_x, bg_y = -(BACKGROUND_WIDTH - SCREEN_WIDTH) // 2, -(BACKGROUND_HEIGHT - SCREEN_HEIGHT) // 2
    vida_actual = vida_maxima
    dentro_casa = None
    cinematica = None
    game_over = False

# Función principal del juego
def iniciar_juego():
    global antonio_x, antonio_y, dentro_casa, cinematica, game_over, vida_actual, bg_x, bg_y

    while True:
        screen.blit(background, (bg_x, bg_y))  # Dibujar fondo en movimiento
        dibujar_barra_vida()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                dentro_casa = None

        # Movimiento del personaje y del fondo
        keys = pygame.key.get_pressed()

        # Movimiento vertical
        if keys[pygame.K_w]:  # Arriba
            if antonio_y > MARGIN_Y or bg_y >= 0:
                antonio_y = max(antonio_y - delta, 0)
            else:
                bg_y = min(bg_y + delta, 0)
        if keys[pygame.K_s]:  # Abajo
            if antonio_y < SCREEN_HEIGHT - MARGIN_Y or bg_y <= SCREEN_HEIGHT - BACKGROUND_HEIGHT:
                antonio_y = min(antonio_y + delta, SCREEN_HEIGHT - 50)
            else:
                bg_y = max(bg_y - delta, SCREEN_HEIGHT - BACKGROUND_HEIGHT)

        # Movimiento horizontal
        if keys[pygame.K_a]:  # Izquierda
            if antonio_x > MARGIN_X or bg_x >= 0:
                antonio_x = max(antonio_x - delta, 0)
            else:
                bg_x = min(bg_x + delta, 0)
        if keys[pygame.K_d]:  # Derecha
            if antonio_x < SCREEN_WIDTH - MARGIN_X or bg_x <= SCREEN_WIDTH - BACKGROUND_WIDTH:
                antonio_x = min(antonio_x + delta, SCREEN_WIDTH - 50)
            else:
                bg_x = max(bg_x - delta, SCREEN_WIDTH - BACKGROUND_WIDTH)

        # Dibujar personaje
        screen.blit(antonio_img, (antonio_x - 25, antonio_y - 25))

        pygame.display.flip()
        clock.tick(30)

# Función principal
def main():
    while True:
        pantalla_inicio()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reiniciar_juego()
                    iniciar_juego()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        clock.tick(30)

# Iniciar el juego
main()
s