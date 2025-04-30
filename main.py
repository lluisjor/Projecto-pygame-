import pygame
import json
import os
import math

# Inicializar Pygame
pygame.init()

# Configuración de pantalla con tamaño fijo
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 902
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Antonio Recio: El Imperio del Marisco")

# Cargar música para el menú
pygame.mixer.music.load("static/lqsa.mp3")
pygame.mixer.music.set_volume(0.5)

# Cargar sonido para disparo
sonido_disparo = pygame.mixer.Sound("static/lqsa.mp3")
sonido_disparo.set_volume(0.5)

# Cargar imagen de fondo
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 3000, 2000
background = pygame.image.load("static/lqsa2.png")
background = pygame.transform.scale(background, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

# Cargar imagen del personaje
antonio_img = pygame.image.load("static/antonio.png")
antonio_img = pygame.transform.scale(antonio_img, (50, 50))

# Cargar imagen de fondo para el menú
menu_background = pygame.image.load("static/fondo.png")
menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Posición inicial del personaje
antonio_x, antonio_y = BACKGROUND_WIDTH // 2, BACKGROUND_HEIGHT // 2

# Velocidad del personaje
velocidad = 5

# Barra de vida
vida_maxima = 100
vida_actual = vida_maxima

# Reloj para control de FPS
clock = pygame.time.Clock()

# Lista de proyectiles
proyectiles = []

# Función para dibujar barra de vida
def dibujar_barra_vida():
    pygame.draw.rect(screen, (139, 0, 0), (10, 10, 300, 30))
    color_vida = (0, 255, 0) if vida_actual > 70 else (255, 255, 0) if vida_actual > 30 else (200, 0, 0)
    pygame.draw.rect(screen, color_vida, (10, 10, (vida_actual / vida_maxima) * 300, 30))


# Clase Proyectil
class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((20, 10))
        self.image.fill((255, 0, 0))  # Rojo, puedes cambiarlo
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = angle
        self.velocidad = 10  # Velocidad del proyectil

    def update(self):
        # Movimiento del proyectil en la dirección del ángulo
        self.rect.x += self.velocidad * math.cos(self.angle)
        self.rect.y += self.velocidad * math.sin(self.angle)

        # Eliminar proyectil si sale de la pantalla
        if not screen.get_rect().colliderect(self.rect):
            self.kill()


# Menú de pausa
def pausa():
    font = pygame.font.Font(None, 48)
    texto_continuar = font.render("Presiona O para continuar", True, (255, 255, 255))
    texto_guardar = font.render("Presiona G para guardar partida", True, (255, 255, 255))
    texto_salir = font.render("Presiona ESC para salir del juego", True, (255, 255, 255))

    pausado = True
    while pausado:
        screen.fill((0, 0, 0))
        screen.blit(texto_continuar, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 80))
        screen.blit(texto_guardar, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
        screen.blit(texto_salir, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 80))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    pausado = False
                elif event.key == pygame.K_g:
                    guardar_partida()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


# Pantalla de inicio
def pantalla_inicio():
    pygame.mixer.music.play(-1)
    font = pygame.font.Font(None, 48)
    texto_jugar = font.render("Presiona ENTER para Jugar", True, (255, 255, 255))
    texto_cargar = font.render("Presiona C para Cargar Partida", True, (255, 255, 255))
    texto_salir = font.render("Presiona ESC para Salir", True, (255, 255, 255))

    while True:
        screen.blit(menu_background, (0, 0))
        screen.blit(texto_jugar, (SCREEN_WIDTH // 2 - texto_jugar.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(texto_cargar, (SCREEN_WIDTH // 2 - texto_cargar.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(texto_salir, (SCREEN_WIDTH // 2 - texto_salir.get_width() // 2, SCREEN_HEIGHT // 2 + 80))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    iniciar_juego()
                elif event.key == pygame.K_c:
                    cargar_partida()
                    pygame.mixer.music.stop()
                    iniciar_juego()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return


# Función principal del juego
def iniciar_juego():
    global antonio_x, antonio_y

    running = True
    while running:
        screen.blit(background, (0, 0))
        dibujar_barra_vida()
        screen.blit(antonio_img, (antonio_x, antonio_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Captura las teclas presionadas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            antonio_y -= velocidad
        if keys[pygame.K_s]:
            antonio_y += velocidad
        if keys[pygame.K_a]:
            antonio_x -= velocidad
        if keys[pygame.K_d]:
            antonio_x += velocidad
        if keys[pygame.K_p]:
            pausa()

        # Disparo
        if keys[pygame.K_SPACE]:
            angle = math.radians(0)  # Disparo hacia la derecha (puedes ajustar el ángulo si quieres)
            proyectil = Proyectil(antonio_x + 50, antonio_y + 25, angle)  # Crear proyectil en la posición de Antonio
            proyectiles.append(proyectil)  # Añadir proyectil a la lista
            sonido_disparo.play()  # Reproducir sonido de disparo

        # Actualizar proyectiles
        for proyectil in proyectiles:
            proyectil.update()
            screen.blit(proyectil.image, proyectil.rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


# Iniciar pantalla principal
pantalla_inicio()
