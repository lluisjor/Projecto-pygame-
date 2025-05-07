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

# Cargar sonidos
robo_sonido = pygame.mixer.Sound("static/mario-coin.mp3")
sonido_ascensor = pygame.mixer.Sound("static/moroso.mp3")
sonido_ascensor.set_volume(0.5)

# Fondos del juego
background_1 = pygame.image.load("static/la-que-se-avecina-pixilart (12) (3).png")
BACKGROUND_WIDTH_1, BACKGROUND_HEIGHT_1 = background_1.get_size()
background_2 = pygame.image.load("static/rellanoo (2).png")
BACKGROUND_WIDTH_2, BACKGROUND_HEIGHT_2 = background_2.get_size()

# Fondo del menú
menu_background = pygame.image.load("static/fondo.png")
menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Personajes
antonio_img = pygame.image.load("static/antonio.png")
antonio_img = pygame.transform.scale(antonio_img, (50, 50))
enrique_img = pygame.image.load("static/enrique.png")
enrique_img = pygame.transform.scale(enrique_img, (50, 50))
calvo_img = pygame.image.load("static/enrique.png")
calvo_img = pygame.transform.scale(calvo_img, (50, 50))

# Imágenes de eventos
llave_img = pygame.image.load("static/llave.png")
llave_img = pygame.transform.scale(llave_img, (400, 300))
caja_fuerte_img = pygame.image.load("static/cajafuerte.png")
caja_fuerte_img = pygame.transform.scale(caja_fuerte_img, (400, 300))

# Reloj y fuente
clock = pygame.time.Clock()
fuente = pygame.font.Font(None, 50)

# Variables de Antonio
antonio_x, antonio_y = BACKGROUND_WIDTH_1 // 2, BACKGROUND_HEIGHT_1 // 2
velocidad = 6

# Posición estática de Enrique
enrique_x, enrique_y = 2148, 1485

# Zonas de interacción
KEY_ZONE = pygame.Rect(310, 260, 50, 50)
SAFE_ZONE = pygame.Rect(830, 890, 50, 50)

# Estados de misión
obtuvo_llave = False
dinero_robado = False
pantalla_actual = 1

# Diálogos
dialogo_inicial = [
    "Enrique: ¡Bienvenido a mi casa!",
    "Antonio: Vine a cobrar la deuda.",
    "Enrique: Está en el cajón de la derecha.",
    "Antonio: Gracias, ahora me voy."
]
dialogo_pelea = [
    "Enrique: ¡Vas a pagar por esto!",
    "Antonio: ¡No te asustes, calvo!"
]


def generar_paredes_desde_imagen(imagen, escala=10):
    paredes = []
    ancho, alto = imagen.get_size()
    imagen = pygame.transform.scale(imagen, (ancho // escala, alto // escala))
    pixeles = pygame.PixelArray(imagen)
    for y in range(imagen.get_height()):
        for x in range(imagen.get_width()):
            color = imagen.unmap_rgb(pixeles[x, y])
            if color == (0, 0, 0):
                rect = pygame.Rect(x * escala, y * escala, escala, escala)
                paredes.append(rect)
    del pixeles
    return paredes


mapa_img_1 = background_1.convert()
mapa_img_2 = background_2.convert()
paredes_mapa_1 = generar_paredes_desde_imagen(mapa_img_1, escala=10)
paredes_mapa_2 = generar_paredes_desde_imagen(mapa_img_2, escala=10)


def mostrar_menu():
    pygame.mixer.music.play(-1)
    en_menu = True
    while en_menu:
        screen.blit(menu_background, (0, 0))
        screen.blit(fuente.render("ANTONIO RECIO: EL IMPERIO DEL MARISCO", True, (255, 255, 255)),
                    (SCREEN_WIDTH // 2 - 400, SCREEN_HEIGHT // 2 - 100))
        screen.blit(fuente.render("ENTER: Jugar   C: Cargar   ESC: Salir", True, (255, 255, 255)),
                    (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 20))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_RETURN, pygame.K_c):
                    pygame.mixer.music.stop(); en_menu = False
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); exit()


def pausa():
    sonido = pygame.mixer.Sound("static/lqsa.mp3")
    sonido.play()
    opciones = [fuente.render("O: continuar", True, (255, 255, 255)),
                fuente.render("ESC: salir", True, (255, 255, 255))]
    while True:
        screen.fill((0, 0, 0))
        screen.blit(opciones[0], (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30))
        screen.blit(opciones[1], (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 30))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_o:
                    sonido.stop(); return
                if e.key == pygame.K_ESCAPE:
                    sonido.stop(); pygame.quit(); exit()


def transicion_fundido(color=(0, 0, 0), vel=15):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade.fill(color)
    for a in range(0, 255, vel):
        fade.set_alpha(a)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)


def mostrar_mensaje(texto):
    msg = fuente.render(texto, True, (255, 255, 255))
    screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 50))
    pygame.display.flip()
    pygame.time.delay(1500)


def mostrar_cuadro_dialogo(linea):
    alto = 120
    s = pygame.Surface((SCREEN_WIDTH - 100, alto))
    s.set_alpha(200); s.fill((0, 0, 0))
    screen.blit(s, (50, SCREEN_HEIGHT - alto - 50))
    pygame.draw.rect(screen, (255, 255, 255), (50, SCREEN_HEIGHT - alto - 50, SCREEN_WIDTH - 100, alto), 3)
    txt = fuente.render(linea, True, (255, 255, 255))
    screen.blit(txt, (70, SCREEN_HEIGHT - alto + 10))
    pygame.display.flip()


def mostrar_imagen_temporal(imagen, duracion_ms=2000):
    screen.blit(imagen, (SCREEN_WIDTH // 2 - imagen.get_width() // 2, SCREEN_HEIGHT // 2 - imagen.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(duracion_ms)


def mostrar_imagen_y_musica_en_ascensor():
    imagen_ascensor = pygame.image.load("static/ascensor.png")
    imagen_ascensor = pygame.transform.scale(imagen_ascensor, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(imagen_ascensor, (0, 0))
    pygame.display.flip()
    pygame.mixer.music.play(-1)
    pygame.time.delay(8000)
    pygame.mixer.music.stop()


def jugar():
    global antonio_x, antonio_y, pantalla_actual, obtuvo_llave, dinero_robado

    ascensor_cd = 0
    dialogo_visible = False
    idx_dialogo = 0
    dialogo_list = dialogo_inicial

    while True:
        screen.fill((0, 0, 0))

        if pantalla_actual == 1:
            bg, bw, bh = background_1, BACKGROUND_WIDTH_1, BACKGROUND_HEIGHT_1
            paredes_actuales = paredes_mapa_1
        else:
            bg, bw, bh = background_2, BACKGROUND_WIDTH_2, BACKGROUND_HEIGHT_2
            paredes_actuales = paredes_mapa_2

        cam_x = max(0, min(antonio_x - SCREEN_WIDTH // 2, bw - SCREEN_WIDTH))
        cam_y = max(0, min(antonio_y - SCREEN_HEIGHT // 2, bh - SCREEN_HEIGHT))
        screen.blit(bg, (-cam_x, -cam_y))

        keys = pygame.key.get_pressed()
        screen.blit(antonio_img, (antonio_x - cam_x, antonio_y - cam_y))

        if pantalla_actual == 1:
            e_rect = pygame.Rect(enrique_x, enrique_y, 50, 50)
            screen.blit(enrique_img, (enrique_x - cam_x, enrique_y - cam_y))
            a_rect = pygame.Rect(antonio_x, antonio_y, 50, 50)
            if a_rect.colliderect(e_rect) and not dialogo_visible:
                screen.blit(fuente.render("E: Hablar", True, (255, 255, 255)),
                            (enrique_x - cam_x, enrique_y - cam_y - 30))
                if keys[pygame.K_e]:
                    dialogo_visible = True
                    idx_dialogo = 0
                    if dinero_robado:
                        dialogo_list = dialogo_pelea

        if dialogo_visible:
            if idx_dialogo < len(dialogo_list):
                mostrar_cuadro_dialogo(dialogo_list[idx_dialogo])
                if keys[pygame.K_SPACE]:
                    pygame.time.delay(200)
                    idx_dialogo += 1
            else:
                dialogo_visible = False

        if pantalla_actual == 1 and not obtuvo_llave:
            zr = KEY_ZONE.move(-cam_x, -cam_y)
            pygame.draw.rect(screen, (255, 255, 0), zr, 2)
            if zr.colliderect(pygame.Rect(antonio_x - cam_x, antonio_y - cam_y, 50, 50)):
                screen.blit(fuente.render("E: Robar llave", True, (255, 255, 255)),
                            (zr.x, zr.y - 30))
                if keys[pygame.K_e]:
                    obtuvo_llave = True
                    mostrar_imagen_temporal(llave_img)
                    mostrar_mensaje("Has robado la llave maestra")

        if pantalla_actual == 2 and not dinero_robado:
            sd = SAFE_ZONE.move(-cam_x, -cam_y)
            pygame.draw.rect(screen, (255, 0, 0), sd, 2)
            if sd.colliderect(pygame.Rect(antonio_x - cam_x, antonio_y - cam_y, 50, 50)):
                screen.blit(fuente.render("E: Robar dinero", True, (255, 255, 255)),
                            (sd.x, sd.y - 30))
                if keys[pygame.K_e] and obtuvo_llave:
                    dinero_robado = True
                    robo_sonido.play()
                    mostrar_imagen_temporal(caja_fuerte_img)

                    for _ in range(3):
                        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                        overlay.set_alpha(120)
                        overlay.fill((0, 255, 0))
                        screen.blit(overlay, (0, 0))
                        pygame.display.flip()
                        pygame.time.delay(100)
                        screen.blit(bg, (-cam_x, -cam_y))
                        screen.blit(antonio_img, (antonio_x - cam_x, antonio_y - cam_y))
                        pygame.display.flip()
                        pygame.time.delay(100)

                    mostrar_mensaje("Has robado 10.000€ del cajón fuerte")
                    pygame.time.delay(500)

        if pantalla_actual == 2 and dinero_robado:
            hud_text = fuente.render("Dinero robado: 10.000€", True, (255, 255, 0))
            screen.blit(hud_text, (SCREEN_WIDTH - hud_text.get_width() - 20, 20))

        if not dialogo_visible:
            nueva_x, nueva_y = antonio_x, antonio_y
            if keys[pygame.K_w]: nueva_y -= velocidad
            if keys[pygame.K_s]: nueva_y += velocidad
            if keys[pygame.K_a]: nueva_x -= velocidad
            if keys[pygame.K_d]: nueva_x += velocidad
            rect_nuevo = pygame.Rect(nueva_x, nueva_y, 50, 50)
            colisiona = any(rect_nuevo.colliderect(p) for p in paredes_actuales)
            if not colisiona:
                antonio_x, antonio_y = nueva_x, nueva_y
            if keys[pygame.K_p]: pausa()

        antonio_x = max(0, min(antonio_x, bw - 50))
        antonio_y = max(0, min(antonio_y, bh - 50))

        asc_x, asc_y = (830, 550) if pantalla_actual == 1 else (1005, 20)
        ar = pygame.Rect(antonio_x, antonio_y, 50, 50)
        asr = pygame.Rect(asc_x, asc_y, 210, 150)
        if ascensor_cd == 0 and ar.colliderect(asr):
            transicion_fundido()
            pantalla_actual = 2 if pantalla_actual == 1 else 1
            if pantalla_actual == 2:
                antonio_x, antonio_y = 1005 + 80, 20 + 30
            else:
                antonio_x, antonio_y = 830 + 80, 550 + 30
            mostrar_imagen_y_musica_en_ascensor()
            ascensor_cd = 60

        if ascensor_cd > 0:
            ascensor_cd -= 1

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); return

        pygame.display.flip()
        clock.tick(60)


# Iniciar juego
mostrar_menu()
jugar()
