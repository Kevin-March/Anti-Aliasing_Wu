import pygame
import math

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Wu Anti-Aliasing vs. Sin Anti-Aliasing')

# Fuente para el texto
font = pygame.font.SysFont(None, 36)

# Función para dibujar un píxel con un color RGB y una intensidad
def plot_pixel(x, y, base_color, intensity=1):
    """Dibuja un píxel en la posición (x, y) con una mezcla de color e intensidad."""
    if 0 <= x < width and 0 <= y < height:
        color = (int(base_color[0] * intensity), 
                 int(base_color[1] * intensity), 
                 int(base_color[2] * intensity))
        screen.set_at((x, y), color)

# Algoritmo básico de línea sin anti-aliasing (similar a Bresenham)
def draw_line_basic(x0, y0, x1, y1, color):
    """Dibuja una línea básica sin anti-aliasing."""
    dx = x1 - x0
    dy = y1 - y0
    steep = abs(dy) > abs(dx)
    
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    
    dx = x1 - x0
    dy = abs(y1 - y0)
    error = dx / 2.0
    ystep = 1 if y0 < y1 else -1
    y = y0
    
    for x in range(x0, x1 + 1):
        if steep:
            plot_pixel(y, x, color)
        else:
            plot_pixel(x, y, color)
        error -= dy
        if error < 0:
            y += ystep
            error += dx

# Algoritmo de Wu para anti-aliasing
def draw_line_wu(x0, y0, x1, y1, color):
    """Dibuja una línea entre (x0, y0) y (x1, y1) utilizando el anti-aliasing de Wu."""
    def fpart(x):
        return x - int(x)

    def rfpart(x):
        return 1 - fpart(x)
    
    steep = abs(y1 - y0) > abs(x1 - x0)
    
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0
    gradient = dy / dx if dx != 0 else 1

    # Dibujar el primer punto
    xend = round(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = rfpart(x0 + 0.5)
    xpxl1 = xend
    ypxl1 = int(yend)
    if steep:
        plot_pixel(ypxl1, xpxl1, color, rfpart(yend) * xgap)
        plot_pixel(ypxl1 + 1, xpxl1, color, fpart(yend) * xgap)
    else:
        plot_pixel(xpxl1, ypxl1, color, rfpart(yend) * xgap)
        plot_pixel(xpxl1, ypxl1 + 1, color, fpart(yend) * xgap)
    intery = yend + gradient

    # Dibujar los puntos del medio
    for x in range(xpxl1 + 1, round(x1)):
        if steep:
            plot_pixel(int(intery), x, color, rfpart(intery))
            plot_pixel(int(intery) + 1, x, color, fpart(intery))
        else:
            plot_pixel(x, int(intery), color, rfpart(intery))
            plot_pixel(x, int(intery) + 1, color, fpart(intery))
        intery += gradient

    # Dibujar el último punto
    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = fpart(x1 + 0.5)
    xpxl2 = xend
    ypxl2 = int(yend)
    if steep:
        plot_pixel(ypxl2, xpxl2, color, rfpart(yend) * xgap)
        plot_pixel(ypxl2 + 1, xpxl2, color, fpart(yend) * xgap)
    else:
        plot_pixel(xpxl2, ypxl2, color, rfpart(yend) * xgap)
        plot_pixel(xpxl2, ypxl2 + 1, color, fpart(yend) * xgap)

# Función para dibujar texto en la pantalla
def draw_text(text, pos):
    """Dibuja texto en la posición dada."""
    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, pos)

# Ejemplo para dibujar dos líneas: una con anti-aliasing y otra sin él
running = True
while running:
    screen.fill((0, 0, 0))  # Limpiar la pantalla con color negro
    
    # Dibujar una línea diagonal sin anti-aliasing
    draw_line_basic(100, 100, 700, 300, (255, 0, 0))  # Línea roja
    draw_text('Línea normal', (50, 50))
    
    # Dibujar una línea diagonal con anti-aliasing de Wu
    draw_line_wu(100, 500, 700, 700, (0, 0, 255))  # Línea azul con anti-aliasing
    draw_text('Línea con Anti-Aliasing de Wu', (50, 450))
    
    # Actualizar la pantalla
    pygame.display.flip()
    
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Salir de Pygame
pygame.quit()
