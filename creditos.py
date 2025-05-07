import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Créditos en Movimiento")

# Fuente para los créditos
font_credits = pygame.font.Font(None, 70)  # Tamaño de la fuente

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cargar logo PNG
try:
    logo = pygame.image.load("logo.png").convert_alpha()
    logo = pygame.transform.scale(logo, (200, 200))  # Ajusta el tamaño si lo necesitas
except:
    print("No se pudo cargar el logo. Asegúrate de que 'logo.png' esté en la misma carpeta.")
    logo = None

# Texto de los créditos
credits_text = [
    " LA QUE SE AVECINA: EL JUEGO",
    "👤 CREADO POR",
    "Raúl · Marc · Pit",
    "🎨 DISEÑO GRÁFICO",
    "Edificio: Marc",
    "Personajes: Raúl",
    "PROGRAMACIÓN",
    "Código: Pit",
    "AGRADECIMIENTOS",
    "A los creadores de La que se avecina",
    "A nuestros amigos y testers",
    "VERSIÓN 1.0 · AÑO 2025",
    "Gracias por jugar!",
    "¡Nos vemos en Mirador de Montepinar!",
    "PULSA ESC PARA SALIR"
]

# Función para mostrar los créditos subiendo desde abajo
def mostrar_creditos():
    y_offset = SCREEN_HEIGHT
    clock = pygame.time.Clock()

    while y_offset > -len(credits_text) * 120:
        screen.fill(BLACK)

        # Mostrar logo si está disponible
        if logo:
            logo_y = SCREEN_HEIGHT // 2 - logo.get_height() // 2
            screen.blit(logo, (SCREEN_WIDTH - logo.get_width() - 50, logo_y))

        # Dibujar cada línea de créditos
        for i, line in enumerate(credits_text):
            credit_line = font_credits.render(line, True, WHITE)
            x = 100  # Posición X (alineado a la izquierda)
            y = y_offset + i * 120
            screen.blit(credit_line, (x, y))

        pygame.display.flip()
        y_offset -= 1.5  # Velocidad de desplazamiento
        clock.tick(60)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Ejecutar los créditos
mostrar_creditos()
