import pygame
import os
import json

# Inicialización
pygame.init()

# Configuración de ventana
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Antonio Recio: El Imperio del Marisco")

# Música
pygame.mixer.music.load("static/lqsa.mp3")
pygame.mixer.music.set_volume(0.6)

# Fondo del juego
background = pygame.image.load("static/lqsa2.png")
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = background.get_size()

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
antonio_x, antonio_y = BACKGROUND_WIDTH // 2, BACKGROUND_HEIGHT // 2
velocidad = 6  # Velocidad del personaje
vida_maxima = 100
vida_actual = vida_maxima

# Área del ascensor (zona azul)
ASCENSOR_X, ASCENSOR_Y = 400, 300
ASCENSOR_ANCHO, ASCENSOR_ALTO = 100, 100

# Función para mostrar el menú principal
def mostrar_menu():
    pygame.mixer.music.play(-1)  # Reproducir música en bucle
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
                    pygame.mixer.music.stop()  # Detener música cuando se inicia el juego
                    en_menu = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_c:
                    cargar_partida()
                    pygame.mixer.music.stop()
                    en_menu = False

# Función para guardar partida
def guardar_partida():
    data = {
        "antonio_x": antonio_x,
        "antonio_y": antonio_y,
        "vida_actual": vida_actual
    }
    with open("savegame.json", "w") as f:
        json.dump(data, f)
    print("Partida guardada.")

# Función para cargar partida
def cargar_partida():
    global antonio_x, antonio_y, vida_actual
    if os.path.exists("savegame.json"):
        with open("savegame.json", "r") as f:
            data = json.load(f)
            antonio_x = data.get("antonio_x", antonio_x)
            antonio_y = data.get("antonio_y", antonio_y)
            vida_actual = data.get("vida_actual", vida_actual)
        print("Partida cargada.")

# Función de pausa
def pausa():
    sonido_pausa = pygame.mixer.Sound("static/pause_sound.wav")
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
                elif event.key == pygame.K_g:
                    guardar_partida()
                elif event.key == pygame.K_ESCAPE:
                    sonido_pausa.stop()
                    pygame.quit()
                    exit()

# Función principal del juego
def jugar():
    global antonio_x, antonio_y, vida_actual

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Cámara centrada en el personaje
        camera_x = max(0, min(antonio_x - SCREEN_WIDTH // 2, BACKGROUND_WIDTH - SCREEN_WIDTH))
        camera_y = max(0, min(antonio_y - SCREEN_HEIGHT // 2, BACKGROUND_HEIGHT - SCREEN_HEIGHT))

        # Dibujar fondo y jugador
        screen.blit(background, (-camera_x, -camera_y))
        screen.blit(antonio_img, (antonio_x - camera_x, antonio_y - camera_y))

        # Dibujo del ascensor (zona azul visible)
        screen_x = ASCENSOR_X - camera_x
        screen_y = ASCENSOR_Y - camera_y
        pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y, ASCENSOR_ANCHO, ASCENSOR_ALTO), 4)

        # Barra de vida
        pygame.draw.rect(screen, (139, 0, 0), (10, 10, 300, 30))
        color_vida = (0, 255, 0) if vida_actual > 70 else (255, 255, 0) if vida_actual > 30 else (200, 0, 0)
        pygame.draw.rect(screen, color_vida, (10, 10, (vida_actual / vida_maxima) * 300, 30))

        # Controles
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Iniciar el juego
mostrar_menu()
jugar()
