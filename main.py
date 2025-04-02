import pygame

# Inicializar Pygame
pygame.init()

# Configuración de pantalla con tamaño fijo
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 902
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Antonio Recio: El Imperio del Marisco")

# Cargar imagen de fondo y ajustarla al tamaño de la pantalla
background = pygame.image.load("/mnt/data/lqsa.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cargar imagen del personaje
antonio_img = pygame.image.load("static/enrique.png")
antonio_img = pygame.transform.scale(antonio_img, (50, 50))

# Posición inicial del personaje (centrado en la pantalla)
antonio_x, antonio_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()


def iniciar_juego():
    global antonio_x, antonio_y

    running = True
    while running:
        screen.blit(background, (0, 0))  # Dibujar fondo en la pantalla
        screen.blit(antonio_img, (antonio_x - 25, antonio_y - 25))  # Dibujar personaje centrado

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(30)  # Limitar FPS

    pygame.quit()


# Iniciar el juego
iniciar_juego()
