import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Antonio Recio: El Imperio del Marisco")

# Colores
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 255, 0)  # Color para la barra de vida
YELLOW = (255, 255, 0)  # Color intermedio para la vida
DARK_RED = (139, 0, 0)  # Fondo de la barra de vida
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # Definición del color azul

# Cargar fondo de la portada de inicio
fondo_inicio = pygame.image.load("static/fondo.png")
fondo_inicio = pygame.transform.scale(fondo_inicio, (WIDTH, HEIGHT))

# Cargar fondo
background = pygame.image.load("static/lqsa.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_enrique = pygame.image.load("static/viejas.png")
background_enrique = pygame.transform.scale(background_enrique, (WIDTH, HEIGHT))
background_viejas = pygame.image.load("static/viejas.png")
background_viejas = pygame.transform.scale(background_viejas, (WIDTH, HEIGHT))

# Cargar sprite del personaje
antonio_img = pygame.image.load("static/recio.png")
antonio_img = pygame.transform.scale(antonio_img, (50, 50))

# Cargar sprite de enemigo
enemigo_img = pygame.image.load("static/marc.png")
enemigo_img = pygame.transform.scale(enemigo_img, (50, 50))

# Estados del juego
game_over = False
cinematica = None
dentro_casa = None

# Barra de vida
vida_maxima = 100
vida_actual = vida_maxima

# Reloj
clock = pygame.time.Clock()

# Definición de casas y obstáculos
casas = {
    "Enrique": pygame.Rect(100, 100, 80, 80),
    "Viejas": pygame.Rect(600, 350, 80, 80),
}

# Lista de enemigos
num_enemigos = 3
enemigos = []
for _ in range(num_enemigos):
    enemigo_x = random.randint(0, WIDTH - 50)
    enemigo_y = random.randint(0, HEIGHT - 50)
    enemigos.append({"x": enemigo_x, "y": enemigo_y, "dx": random.choice([-3, 3]), "dy": random.choice([-3, 3])})


# Función para la pantalla de inicio
def pantalla_inicio():
    font = pygame.font.Font(None, 48)
    texto_jugar = font.render("Presiona ENTER para Jugar", True, WHITE)
    texto_salir = font.render("Presiona ESC para Salir", True, WHITE)

    screen.blit(fondo_inicio, (0, 0))  # Mostrar la imagen de fondo

    # Mostrar las opciones en el centro de la pantalla
    screen.blit(texto_jugar, (WIDTH // 2 - texto_jugar.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(texto_salir, (WIDTH // 2 - texto_salir.get_width() // 2, HEIGHT // 2 + 40))

    pygame.display.flip()


# Función para dibujar la barra de vida estilo GTA
def dibujar_barra_vida():
    # Fondo de la barra de vida (oscuro)
    pygame.draw.rect(screen, DARK_RED, (10, 10, 300, 30))

    # Color de la vida (se cambia a amarillo cuando la vida está por debajo de cierto umbral)
    if vida_actual > vida_maxima * 0.7:
        color_vida = GREEN
    elif vida_actual > vida_maxima * 0.3:
        color_vida = YELLOW
    else:
        color_vida = RED

    # Barra de vida actual
    pygame.draw.rect(screen, color_vida, (10, 10, (vida_actual / vida_maxima) * 300, 30))


# Función para reiniciar el juego
def reiniciar_juego():
    global antonio_x, antonio_y, vida_actual, enemigos, dentro_casa, cinematica, game_over
    antonio_x, antonio_y = WIDTH // 2, HEIGHT // 2
    vida_actual = vida_maxima  # Regenerar vida
    enemigos = []  # Reiniciar lista de enemigos

    # Volver a crear los enemigos con posiciones aleatorias
    for _ in range(3):
        enemigo_x = random.randint(0, WIDTH - 50)
        enemigo_y = random.randint(0, HEIGHT - 50)
        enemigos.append({"x": enemigo_x, "y": enemigo_y, "dx": random.choice([-3, 3]), "dy": random.choice([-3, 3])})

    dentro_casa = None  # Reiniciar el estado de las casas
    cinematica = None  # Reiniciar cualquier mensaje de cinemática
    game_over = False  # Reiniciar el estado de Game Over


# Función principal del juego
def iniciar_juego():
    global antonio_x, antonio_y, dentro_casa, cinematica, game_over, vida_actual, enemigos

    while True:
        if dentro_casa == "Enrique":
            screen.blit(background_enrique, (0, 0))
        elif dentro_casa == "Viejas":
            screen.blit(background_viejas, (0, 0))
        else:
            screen.blit(background, (0, 0))

        # Dibujar la barra de vida estilo GTA
        dibujar_barra_vida()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Salir del juego
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                dentro_casa = None

        # Movimiento del personaje
        new_x, new_y = antonio_x, antonio_y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            new_x -= 5
        if keys[pygame.K_RIGHT]:
            new_x += 5
        if keys[pygame.K_UP]:
            new_y -= 5
        if keys[pygame.K_DOWN]:
            new_y += 5

        # Crear un rectángulo con la nueva posición
        antonio_rect = pygame.Rect(new_x, new_y, 50, 50)

        # Verificar colisiones con casas y obstáculos
        obstaculos = [
                         pygame.Rect(200, 50, 100, 100),  # Casa 1
                         pygame.Rect(400, 50, 100, 100),  # Casa 2
                         pygame.Rect(600, 50, 100, 100),  # Casa 3
                         pygame.Rect(100, 300, 150, 100),  # Casa 4
                         pygame.Rect(500, 300, 150, 100),  # Casa 5
                     ] + list(casas.values())  # Se agregan las casas como obstáculos
        colision = any(antonio_rect.colliderect(obst) for obst in obstaculos)

        # Si no hay colisión, mover a Antonio
        if not colision:
            antonio_x, antonio_y = new_x, new_y

        # Dibujar personaje
        screen.blit(antonio_img, (antonio_x, antonio_y))

        if dentro_casa is None:
            # Dibujar casas
            for casa in casas.values():
                pygame.draw.rect(screen, BLUE, casa)

            # Verificar colisiones con puertas
            for nombre, casa in casas.items():
                if antonio_rect.colliderect(casa):
                    cinematica = f"Antonio entra en la casa de {nombre}..."
                    dentro_casa = nombre

        # Dibujar enemigos y moverlos
        for enemigo in enemigos:
            enemigo["x"] += enemigo["dx"]
            enemigo["y"] += enemigo["dy"]

            # Rebotar en los bordes de la pantalla
            if enemigo["x"] <= 0 or enemigo["x"] >= WIDTH - 50:
                enemigo["dx"] = -enemigo["dx"]
            if enemigo["y"] <= 0 or enemigo["y"] >= HEIGHT - 50:
                enemigo["dy"] = -enemigo["dy"]

            screen.blit(enemigo_img, (enemigo["x"], enemigo["y"]))

            # Colisión con Antonio
            if antonio_rect.colliderect(pygame.Rect(enemigo["x"], enemigo["y"], 50, 50)):
                antonio_x, antonio_y = WIDTH // 2, HEIGHT // 2
                vida_actual -= 10  # Pierde 10 de vida cada vez que es atrapado por un enemigo
                print("¡Te atraparon!")
                if vida_actual <= 0:
                    game_over = True
                    print("¡Game Over!")
                    return False  # Fin del juego

        # Mostrar cinemática
        if cinematica:
            font = pygame.font.Font(None, 36)
            texto = font.render(cinematica, True, BLACK)
            screen.blit(texto, (50, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            cinematica = None

        pygame.display.flip()
        clock.tick(30)


# Función principal
def main():
    jugando = True
    while jugando:
        pantalla_inicio()

        # Esperar una entrada para decidir jugar o salir
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter para jugar
                    reiniciar_juego()  # Reiniciar el juego
                    iniciar_juego()
                elif event.key == pygame.K_ESCAPE:  # Escape para salir
                    pygame.quit()
                    return

        clock.tick(30)


# Iniciar el juego
main()
