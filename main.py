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

# Fondos
background_main = pygame.image.load("static/lqsa2.png")
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = background_main.get_size()

background_rellano = pygame.image.load("static/rellano.png")
rellano_WIDTH, rellano_HEIGHT = background_rellano.get_size()

# Fondo del menú
menu_background = pygame.image.load("static/fondo.png")
menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Personaje principal
antonio_img = pygame.image.load("static/antonio.png")
antonio_img = pygame.transform.scale(antonio_img, (50, 50))

# Enrique Pastor
enrique_img = pygame.image.load("static/enrique.png")
enrique_img = pygame.transform.scale(enrique_img, (50, 50))
enrique_pos = (600, 300)

# Dinero escondido
dinero_img = pygame.image.load("static/dinero.png")
dinero_img = pygame.transform.scale(dinero_img, (40, 40))
dinero_visible = False
dinero_recogido = False
dinero_pos = (800, 200)

# Reloj
clock = pygame.time.Clock()

# Fuente
fuente = pygame.font.Font(None, 50)
fuente_peque = pygame.font.Font(None, 32)

# Variables de juego
antonio_x, antonio_y = BACKGROUND_WIDTH // 2, BACKGROUND_HEIGHT // 2
velocidad = 6
vida_maxima = 100
vida_actual = vida_maxima

# Estado
en_rellano = False
mision_activa = False

# Función para mostrar el menú principal
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

# Función para guardar partida
def guardar_partida():
    data = {
        "antonio_x": antonio_x,
        "antonio_y": antonio_y,
        "vida_actual": vida_actual,
        "en_rellano": en_rellano,
        "mision_activa": mision_activa,
        "dinero_recogido": dinero_recogido
    }
    with open("savegame.json", "w") as f:
        json.dump(data, f)
    print("Partida guardada.")

# Función para cargar partida
def cargar_partida():
    global antonio_x, antonio_y, vida_actual, en_rellano, mision_activa, dinero_recogido
    if os.path.exists("savegame.json"):
        with open("savegame.json", "r") as f:
            data = json.load(f)
            antonio_x = data.get("antonio_x", antonio_x)
            antonio_y = data.get("antonio_y", antonio_y)
            vida_actual = data.get("vida_actual", vida_actual)
            en_rellano = data.get("en_rellano", False)
            mision_activa = data.get("mision_activa", False)
            dinero_recogido = data.get("dinero_recogido", False)
        print("Partida cargada.")

# Función de pausa
def pausa():
    font = pygame.font.Font(None, 50)
    texto_continuar = font.render("Presiona O para continuar", True, (255, 255, 255))
    texto_guardar = font.render("Presiona G para guardar partida", True, (255, 255, 255))
    texto_salir = font.render("Presiona ESC para salir del juego", True, (255, 255, 255))
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
                    pausado = False
                elif event.key == pygame.K_g:
                    guardar_partida()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# Función principal del juego
def jugar():
    global antonio_x, antonio_y, vida_actual, en_rellano, mision_activa, dinero_recogido

    running = True
    while running:
        screen.fill((0, 0, 0))

        background = background_rellano if en_rellano else background_main
        BACKGROUND_W, BACKGROUND_H = (rellano_WIDTH, rellano_HEIGHT) if en_rellano else (BACKGROUND_WIDTH, BACKGROUND_HEIGHT)

        camera_x = max(0, min(antonio_x - SCREEN_WIDTH // 2, BACKGROUND_W - SCREEN_WIDTH))
        camera_y = max(0, min(antonio_y - SCREEN_HEIGHT // 2, BACKGROUND_H - SCREEN_HEIGHT))

        screen.blit(background, (-camera_x, -camera_y))
        screen.blit(antonio_img, (antonio_x - camera_x, antonio_y - camera_y))

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

        if not en_rellano:
            enrique_rect = pygame.Rect(enrique_pos[0], enrique_pos[1], 50, 50)
            antonio_rect = pygame.Rect(antonio_x, antonio_y, 50, 50)
            screen.blit(enrique_img, (enrique_pos[0] - camera_x, enrique_pos[1] - camera_y))
            if antonio_rect.colliderect(enrique_rect):
                texto = fuente_peque.render("Presiona E para hablar con Enrique", True, (255, 255, 255))
                screen.blit(texto, (antonio_x - camera_x, antonio_y - camera_y - 30))
                if keys[pygame.K_e]:
                    mision_activa = True

        if not en_rellano and antonio_y < 100:
            en_rellano = True
            antonio_x, antonio_y = 500, rellano_HEIGHT - 100

        if en_rellano and mision_activa and not dinero_recogido:
            dinero_rect = pygame.Rect(dinero_pos[0], dinero_pos[1], 40, 40)
            screen.blit(dinero_img, (dinero_pos[0] - camera_x, dinero_pos[1] - camera_y))
            antonio_rect = pygame.Rect(antonio_x, antonio_y, 50, 50)
            if antonio_rect.colliderect(dinero_rect):
                texto = fuente_peque.render("Presiona E para coger el dinero", True, (255, 255, 255))
                screen.blit(texto, (antonio_x - camera_x, antonio_y - camera_y - 30))
                if keys[pygame.K_e]:
                    dinero_recogido = True

        if dinero_recogido:
            screen.blit(fuente_peque.render("¡Has conseguido el dinero!", True, (0, 255, 0)), (50, 650))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

mostrar_menu()
jugar()