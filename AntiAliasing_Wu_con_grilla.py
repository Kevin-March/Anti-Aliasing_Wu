import pygame
import math
import time

# Ancho y alto teórico
ancho_teorico = 600
alto_teorico = 600

# Ancho y alto real
ancho_real = 50
alto_real = 50

# Relation (ratio) de aspecto entre el real y el teórico
delta_x = int(ancho_teorico/ancho_real)
delta_y = int(alto_teorico/alto_real)

screen = pygame.display.set_mode((ancho_teorico, alto_teorico))
running = True

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRIS = (80, 80, 80)
ROJO = (255, 10, 10)


def dibujar_grilla(screen):
    # Lineas horizontales
    for pos_y in range(0, alto_teorico, delta_y):
        pygame.draw.aaline(screen, GRIS, (0, pos_y), (ancho_teorico, pos_y))

    # Lineas verticales
    for pos_x in range(0, ancho_teorico, delta_x):
        pygame.draw.aaline(screen, GRIS, (pos_x, 0), (pos_x, alto_teorico))


def pixel(screen, x, y, color):
    x = int(x)
    y = int(y)
    if x < 0 or x >= ancho_real or y < 0 or y >= alto_real:
        print(f'Punto incorrecto <{x},{y}>')
        return
    pixel_real = (x*delta_x, (alto_real-y-1)*delta_y, delta_x, delta_y)
    print(f'Pixel real={pixel_real}')
    pygame.draw.rect(screen, color, pixel_real)


def plot(screen, color, x, y, c):
    # Modifica el color original según la intensidad 'c'
    color_mod = (int(color[0] * c), int(color[1] * c), int(color[2] * c))
    pixel(screen, x, y, color_mod)
    pygame.display.flip()  # Actualiza la pantalla para mostrar el píxel dibujado
    time.sleep(0.08)  # Pausa de 90ms para hacerlo más lento


def wu_line(screen, x0, y0, x1, y1, color):
    # Determinar si la línea es más vertical que horizontal
    steep = abs(y1 - y0) > abs(x1 - x0)

    if steep:
        # Intercambia las coordenadas x e y si la línea es empinada
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        # Asegura que la línea se dibuje de izquierda a derecha
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    # Calcular las diferencias y el gradiente de la línea
    dx = x1 - x0
    dy = y1 - y0
    gradient = dy / dx if dx != 0 else 1

    # Inicializar el punto de inicio
    xend = round(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = 1 - (x0 + 0.5) % 1
    xpxl1 = xend  # Primer píxel en x
    ypxl1 = int(yend)

    if steep:
        plot(screen, color, ypxl1, xpxl1, 1 - (yend % 1) * xgap)
        plot(screen, color, ypxl1 + 1, xpxl1, (yend % 1) * xgap)
    else:
        plot(screen, color, xpxl1, ypxl1, 1 - (yend % 1) * xgap)
        plot(screen, color, xpxl1, ypxl1 + 1, (yend % 1) * xgap)

    # Variables iniciales para el bucle principal
    intery = yend + gradient  # Primera intersección y
    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = (x1 + 0.5) % 1
    xpxl2 = xend  # Último píxel en x
    ypxl2 = int(yend)

    # Dibuja el último punto
    if steep:
        plot(screen, color, ypxl2, xpxl2, 1 - (yend % 1) * xgap)
        plot(screen, color, ypxl2 + 1, xpxl2, (yend % 1) * xgap)
    else:
        plot(screen, color, xpxl2, ypxl2, 1 - (yend % 1) * xgap)
        plot(screen, color, xpxl2, ypxl2 + 1, (yend % 1) * xgap)

    # Dibuja la línea entre los puntos inicial y final
    if steep:
        for x in range(xpxl1 + 1, xpxl2):
            plot(screen, color, int(intery), x, 1 - (intery % 1))
            plot(screen, color, int(intery) + 1, x, intery % 1)
            intery += gradient
    else:
        for x in range(xpxl1 + 1, xpxl2):
            plot(screen, color, x, int(intery), 1 - (intery % 1))
            plot(screen, color, x, int(intery) + 1, intery % 1)
            intery += gradient

    # Pausa de 0.5 segundos cuando la línea esté completamente dibujada
    time.sleep(0.5)


# Bucle principal de Pygame
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False
    screen.fill(BLACK)
    dibujar_grilla(screen)

    # Dibujar línea con Xiaolin Wu, pixel por pixel
    wu_line(screen, 10, 30, 40, 10, WHITE)  # Cambia los valores según lo que quieras probar

    pygame.display.flip()

pygame.quit()
