import pygame
import os
import json

pygame.init()

# Configuración de ventana
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Antonio Recio: El Imperio del Marisco")

# Música
pygame.mixer.music.load("static/lqsa.mp3")
pygame.mixer.music.set_volume(0.6)

# Fondos del juego
background_1 = pygame.image.load("static/la-que-se-avecina-pixilart (12) (3).png")
BACKGROUND_WIDTH_1, BACKGROUND_HEIGHT_1 = background_1.get_size()

# SEGUNDO FONDO (rellano o nueva planta)
background_2 = pygame.image.load("static/rellanoo.png")  # Cambia por tu imagen
BACKGROUND_WIDTH_2, BACKGROUND_HEIGHT_2 = background_2.get_size()

# Fondo del menú
menu_background = pygame.image.load("static/fondo.png")
menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Personaje
antonio_img = pygame.image.load("static/antonio.png")
antonio_img = pygame.transform.scale(antonio_img, (50, 50))

# Reloj
clock = pygame.time.Clock()

# Fuente
fuente = pygame.font.Font(None, 50)

# Variables de juego
antonio_x, antonio_y = BACKGROUND_WIDTH_1 // 2, BACKGROUND_HEIGHT_1 // 2
velocidad = 6
vida_maxima = 100
vida_actual = vida_maxima

# Ascensor en la primera pantalla
ASCENSOR_X, ASCENSOR_Y = 830, 550
ASCENSOR_ANCHO, ASCENSOR_ALTO = 196, 122

# Estado actual
pantalla_actual = 1  # 1 = primer mapa, 2 = segundo mapa


def mostrar_menu():
    pygame.mixer.music.play(-1)
    en_menu = True
    while en_menu:
        screen.blit(menu_background, (0, 0))

        titulo = fuente.render("ANTONIO RECIO: EL IMPERIO DEL MARISCO", True, (255, 255, 255))
        jugar = fuente.render("Presiona ENTER para Jugar", True, (255, 255, 255))
        cargar = fuente.render("Presiona C para Cargar Partida", True, (255, 255, 255))
        salir = fuente.render("Presiona ESC para Salir", True, (255, 255, 255))

        screen.blit(titulo, (SCREEN_WIDTH//2 - titulo.get_width()//2, SCREEN_HEIGHT//2 - 100))
        screen.blit(jugar, (SCREEN_WIDTH//2 - jugar.get_width()//2, SCREEN_HEIGHT//2))
        screen.blit(cargar, (SCREEN_WIDTH//2 - cargar.get_width()//2, SCREEN_HEIGHT//2 + 60))
        screen.blit(salir, (SCREEN_WIDTH//2 - salir.get_width()//2, SCREEN_HEIGHT//2 + 120))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    en_menu = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_c:
                    cargar_partida()
                    pygame.mixer.music.stop()
                    en_menu = False


def pausa():
    sonido_pausa = pygame.mixer.Sound("static/videoplayback.mp3")
    sonido_pausa.play()

    texto_continuar = fuente.render("Presiona O para continuar", True, (255, 255, 255))
    texto_guardar = fuente.render("Presiona G para guardar partida", True, (255, 255, 255))
    texto_salir = fuente.render("Presiona ESC para salir del juego", True, (255, 255, 255))

    pausado = True
    while pausado:
        screen.fill((0, 0, 0))
        screen.blit(texto_continuar, (SCREEN_WIDTH // 2 - texto_continuar.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(texto_guardar, (SCREEN_WIDTH // 2 - texto_guardar.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(texto_salir, (SCREEN_WIDTH // 2 - texto_salir.get_width() // 2, SCREEN_HEIGHT // 2 + 80))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    sonido_pausa.stop()
                    pausado = False
                elif event.key == pygame.K_ESCAPE:
                    sonido_pausa.stop()
                    pygame.quit()
                    exit()


def transicion_fundido(color=(0, 0, 0), velocidad=15):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade.fill(color)
    for alpha in range(0, 255, velocidad):
        fade.set_alpha(alpha)
        pygame.display.update()
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)


def jugar():
    global antonio_x, antonio_y, vida_actual, pantalla_actual

    running = True
    while running:
        screen.fill((0, 0, 0))

        if pantalla_actual == 1:
            # ----- PANTALLA 1 -----
            background = background_1
            background_width, background_height = BACKGROUND_WIDTH_1, BACKGROUND_HEIGHT_1
        else:
            # ----- PANTALLA 2 -----
            background = background_2
            background_width, background_height = BACKGROUND_WIDTH_2, BACKGROUND_HEIGHT_2

        camera_x = max(0, min(antonio_x - SCREEN_WIDTH // 2, background_width - SCREEN_WIDTH))
        camera_y = max(0, min(antonio_y - SCREEN_HEIGHT // 2, background_height - SCREEN_HEIGHT))

        # Dibujar fondo
        screen.blit(background, (-camera_x, -camera_y))

        # Dibujar ascensor solo en pantalla 1
        if pantalla_actual == 1:
            screen_x = ASCENSOR_X - camera_x
            screen_y = ASCENSOR_Y - camera_y
            pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y, ASCENSOR_ANCHO, ASCENSOR_ALTO), 4)

        # Dibujar Antonio
        screen.blit(antonio_img, (antonio_x - camera_x, antonio_y - camera_y))

        # Barra de vida
        pygame.draw.rect(screen, (139, 0, 0), (10, 10, 300, 30))
        color_vida = (0, 255, 0) if vida_actual > 70 else (255, 255, 0) if vida_actual > 30 else (200, 0, 0)
        pygame.draw.rect(screen, color_vida, (10, 10, (vida_actual / vida_maxima) * 300, 30))

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

        # 🚧 LÍMITES del mapa
        antonio_x = max(0, min(antonio_x, background_width - antonio_img.get_width()))
        antonio_y = max(0, min(antonio_y, background_height - antonio_img.get_height()))

        # Detectar entrada en ascensor (solo en pantalla 1)
        if pantalla_actual == 1:
            antonio_rect = pygame.Rect(antonio_x, antonio_y, antonio_img.get_width(), antonio_img.get_height())
            ascensor_rect = pygame.Rect(ASCENSOR_X, ASCENSOR_Y, ASCENSOR_ANCHO, ASCENSOR_ALTO)

            if antonio_rect.colliderect(ascensor_rect):
                print("¡Entraste al ascensor! Transición...")
                transicion_fundido()
                # Mover a pantalla 2
                pantalla_actual = 2
                # Reseteamos la posición en la nueva pantalla
                antonio_x, antonio_y = BACKGROUND_WIDTH_2 // 2, BACKGROUND_HEIGHT_2 // 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


mostrar_menu()
jugar()
