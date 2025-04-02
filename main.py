import pygame

# Inicializar Pygame
pygame.init()

# Configuración de pantalla con tamaño más pequeño (menos zoom)
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 902  # Reducir el tamaño de la pantalla para obtener más fondo visible
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Antonio Recio: El Imperio del Marisco")

# Cargar música para el menú
pygame.mixer.music.load("static/lqsa.mp3")
pygame.mixer.music.set_volume(0.5)

# Cargar imagen de fondo (escenario más grande que la pantalla)
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 3000, 2000
background = pygame.image.load("static/lqsa.png")
background = pygame.transform.scale(background, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

# Cargar imagen del personaje y reducir su tamaño (hacerlo más pequeño para menos zoom)
antonio_img = pygame.image.load("static/antonio.png")
antonio_img = pygame.transform.scale(antonio_img, (40, 40))  # Reducir tamaño del personaje

# Posición inicial del personaje (centrado en el mapa)
antonio_x, antonio_y = BACKGROUND_WIDTH // 2, BACKGROUND_HEIGHT // 2

# Velocidad del personaje
velocidad = 5

# Barra de vida
vida_maxima = 100
vida_actual = vida_maxima


def dibujar_barra_vida():
    pygame.draw.rect(screen, (139, 0, 0), (10, 10, 300, 30))
    color_vida = (0, 255, 0) if vida_actual > 70 else (255, 255, 0) if vida_actual > 30 else (200, 0, 0)
    pygame.draw.rect(screen, color_vida, (10, 10, (vida_actual / vida_maxima) * 300, 30))


# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()


def pantalla_inicio():
    pygame.mixer.music.play(-1)  # Reproducir música en bucle
    font = pygame.font.Font(None, 48)
    texto_jugar = font.render("Presiona ENTER para Jugar", True, (255, 255, 255))
    texto_salir = font.render("Presiona ESC para Salir", True, (255, 255, 255))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(texto_jugar, (SCREEN_WIDTH // 2 - texto_jugar.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
        screen.blit(texto_salir, (SCREEN_WIDTH // 2 - texto_salir.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    iniciar_juego()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return


def iniciar_juego():
    global antonio_x, antonio_y

    running = True
    while running:
        # Calcular posición de la cámara para que el personaje siempre esté centrado
        camera_x = max(0, min(antonio_x - SCREEN_WIDTH // 2, BACKGROUND_WIDTH - SCREEN_WIDTH))
        camera_y = max(0, min(antonio_y - SCREEN_HEIGHT // 2, BACKGROUND_HEIGHT - SCREEN_HEIGHT))

        # Asegurarse de que la parte inferior del personaje sea visible
        if antonio_y + 40 > SCREEN_HEIGHT:
            camera_y = min(camera_y, BACKGROUND_HEIGHT - SCREEN_HEIGHT)

        screen.blit(background, (-camera_x, -camera_y))  # Dibujar fondo en la posición correcta
        dibujar_barra_vida()  # Dibujar barra de vida
        screen.blit(antonio_img, (antonio_x - camera_x, antonio_y - camera_y))  # Dibujar personaje correctamente

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and antonio_y > 0:
            antonio_y -= velocidad
        if keys[pygame.K_s] and antonio_y < BACKGROUND_HEIGHT - 40:
            antonio_y += velocidad
        if keys[pygame.K_a] and antonio_x > 0:
            antonio_x -= velocidad
        if keys[pygame.K_d] and antonio_x < BACKGROUND_WIDTH - 40:
            antonio_x += velocidad

        pygame.display.flip()
        clock.tick(30)  # Limitar FPS

    pygame.quit()


# Iniciar la pantalla de inicio
pantalla_inicio()
