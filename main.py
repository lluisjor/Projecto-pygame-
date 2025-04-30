import pygame
import os

# Inicialización de Pygame
pygame.init()

# Configuración de ventana
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Antonio Recio: El Imperio del Marisco")

# Música
pygame.mixer.music.load("static/lqsa.mp3")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1)  # Repetir música infinitamente

# Cargar imágenes
background = pygame.image.load("static/lqsa2.png")
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = background.get_size()
menu_background = pygame.image.load("static/fondo.png")
menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

antonio_img = pygame.image.load("static/antonio.png")
antonio_img = pygame.transform.scale(antonio_img, (50, 50))
antonio_x, antonio_y = BACKGROUND_WIDTH // 2, BACKGROUND_HEIGHT // 2
velocidad = 5

# Reloj
clock = pygame.time.Clock()

# Fuente
fuente = pygame.font.Font(None, 50)

# Sonidos
move_sound = pygame.mixer.Sound("static/disparo_marisco.wav")
#impact_sound = pygame.mixer.Sound("static/impact_sound.wav")
#mission_complete_sound = pygame.mixer.Sound("static/mission_complete.wav")

# Función para mostrar el menú principal
def mostrar_menu():
    en_menu = True
    while en_menu:
        screen.blit(menu_background, (0, 0))

        titulo = fuente.render("ANTONIO RECIO: EL IMPERIO DEL MARISCO", True, (255, 255, 255))
        jugar = fuente.render("Presiona ENTER para Jugar", True, (255, 255, 255))
        salir = fuente.render("Presiona ESC para Salir", True, (255, 255, 255))

        screen.blit(titulo, (SCREEN_WIDTH//2 - titulo.get_width()//2, SCREEN_HEIGHT//2 - 100))
        screen.blit(jugar, (SCREEN_WIDTH//2 - jugar.get_width()//2, SCREEN_HEIGHT//2))
        screen.blit(salir, (SCREEN_WIDTH//2 - salir.get_width()//2, SCREEN_HEIGHT//2 + 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    en_menu = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# Función principal del juego
def jugar():
    global antonio_x, antonio_y

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Cámara centrada en el personaje
        camera_x = max(0, min(antonio_x - SCREEN_WIDTH // 2, BACKGROUND_WIDTH - SCREEN_WIDTH))
        camera_y = max(0, min(antonio_y - SCREEN_HEIGHT // 2, BACKGROUND_HEIGHT - SCREEN_HEIGHT))

        # Dibujar fondo y jugador
        screen.blit(background, (-camera_x, -camera_y))
        screen.blit(antonio_img, (antonio_x - camera_x, antonio_y - camera_y))

        # Controles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            antonio_y -= velocidad
            move_sound.play()  # Reproducir sonido de movimiento
        if keys[pygame.K_s]:
            antonio_y += velocidad
            move_sound.play()  # Reproducir sonido de movimiento
        if keys[pygame.K_a]:
            antonio_x -= velocidad
            move_sound.play()  # Reproducir sonido de movimiento
        if keys[pygame.K_d]:
            antonio_x += velocidad
            move_sound.play()  # Reproducir sonido de movimiento

        # Comprobar colisiones con las paredes (en caso de añadir colisiones más tarde)
        # if antonio_x > SCREEN_WIDTH:  # ejemplo de colisión con borde
        #     impact_sound.play()  # Sonido de impacto

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Iniciar el juego
mostrar_menu()
jugar()
