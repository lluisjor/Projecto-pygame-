import pygame
import json
import os

# Inicializar Pygame
pygame.init()

# Configuración de pantalla con tamaño fijo
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 902
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Antonio Recio: El Imperio del Marisco")

# Cargar música para el menú
pygame.mixer.music.load("static/lqsa.mp3")
pygame.mixer.music.set_volume(0.5)

# Cargar sonido de pausa
sonido_pausa = pygame.mixer.Sound("static/lqsa.mp3")
sonido_pausa.set_volume(0.3)

# Cargar imagen de fondo (escenario más grande que la pantalla)
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

# Definir áreas de colisión
paredes = [
    pygame.Rect(0, 0, 500, 500),
    pygame.Rect(600, 400, 800, 200),
    pygame.Rect(1500, 100, 500, 700),
    pygame.Rect(2200, 800, 600, 400)
]

# Área del ascensor
ascensor = pygame.Rect(1200, 800, 100, 100)

# Reloj para control de FPS
clock = pygame.time.Clock()

# Función para dibujar barra de vida
def dibujar_barra_vida():
    pygame.draw.rect(screen, (139, 0, 0), (10, 10, 300, 30))
    color_vida = (0, 255, 0) if vida_actual > 70 else (255, 255, 0) if vida_actual > 30 else (200, 0, 0)
    pygame.draw.rect(screen, color_vida, (10, 10, (vida_actual / vida_maxima) * 300, 30))

# Menú del ascensor
def mostrar_menu_ascensor():
    font = pygame.font.Font(None, 48)
    texto_piso1 = font.render("Presiona 1 para ir al Piso 1", True, (255, 255, 255))
    texto_piso2 = font.render("Presiona 2 para ir al Piso 2", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(texto_piso1, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 40))
    screen.blit(texto_piso2, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 40))
    pygame.display.flip()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2

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

# Menú de pausa
def pausa():
    sonido_pausa.play(-1)  # Inicia sonido de pausa en loop

    font = pygame.font.Font(None, 48)
    texto_continuar = font.render("Presiona P para continuar", True, (255, 255, 255))
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
                sonido_pausa.stop()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    sonido_pausa.stop()  # Detiene el sonido al salir de pausa
                    pausado = False
                elif event.key == pygame.K_g:
                    guardar_partida()
                elif event.key == pygame.K_ESCAPE:
                    sonido_pausa.stop()
                    pygame.quit()
                    exit()

# Pantalla de inicio con imagen de fondo y opciones
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
        camera_x = max(0, min(antonio_x - SCREEN_WIDTH // 2, BACKGROUND_WIDTH - SCREEN_WIDTH))
        camera_y = max(0, min(antonio_y - SCREEN_HEIGHT // 2, BACKGROUND_HEIGHT - SCREEN_HEIGHT))

        screen.blit(background, (-camera_x, -camera_y))
        dibujar_barra_vida()
        screen.blit(antonio_img, (antonio_x - camera_x, antonio_y - camera_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        nuevo_x, nuevo_y = antonio_x, antonio_y
        if keys[pygame.K_w]:
            nuevo_y -= velocidad
        if keys[pygame.K_s]:
            nuevo_y += velocidad
        if keys[pygame.K_a]:
            nuevo_x -= velocidad
        if keys[pygame.K_d]:
            nuevo_x += velocidad
        if keys[pygame.K_p]:
            pausa()

        if not any(p.colliderect(pygame.Rect(nuevo_x, nuevo_y, 50, 50)) for p in paredes):
            antonio_x, antonio_y = nuevo_x, nuevo_y

        if ascensor.colliderect(pygame.Rect(antonio_x, antonio_y, 50, 50)):
            piso = mostrar_menu_ascensor()
            print(f"Viajando al Piso {piso}")

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Iniciar pantalla principal
pantalla_inicio()
