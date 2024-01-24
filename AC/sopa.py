class Cursor:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.avanX = [-1, 0, 1][random.randint(0,2)]
        self.avanY = [-1, 0, 1][random.randint(0,2)]
        if self.avanX == 0 and self.avanY == 0:
            self.avanX = 1

    def next(self, pasos=1):
        self.fila += pasos * self.avanX
        self.columna += pasos * self.avanY

    def es_valido(self, dimension):
        return 0 <= self.fila < dimension and 0 <= self.columna < dimension

    def __str__(self):
        return f"[{self.fila} {self.avanX}, {self.columna} {self.avanY}]"


class Matrix:
    def __init__(self, dimension):
        valores = [' '] * dimension * dimension
        self.dimension = dimension
        self.matriz = np.array(valores).reshape((dimension, dimension))
        self.libres = dimension * dimension
        self.palabras = []

    def __getitem__(self, cursor):
        if cursor.es_valido(self.dimension):
            return self.matriz[cursor.fila][cursor.columna]
        else:
            return ' '

    def __setitem__(self, cursor, value):
        if cursor.es_valido(self.dimension):
            if self.matriz[cursor.fila][cursor.columna] == ' ':
                self.libres -= 1
            self.matriz[cursor.fila][cursor.columna] = value

    def put(self, palabra):
        x, y = random.randint(0, self.dimension - 1), random.randint(0, self.dimension - 1)
        cursor = Cursor(x,y)

        largo = len(palabra)
        cursor.next(largo)
        if not cursor.es_valido(self.dimension):
            return False
        cursor.next(-largo)

        restantes = largo 
        for indice in range(largo):
            if self[cursor] == ' ' or self[cursor] == palabra[indice]:
                self[cursor] = palabra[indice]
                restantes -= 1
            cursor.next()

        if restantes == 0:
            # Esta palabra aparece completa en la matriz
            self.palabras.append((x, y, cursor.avanX, cursor.avanY, palabra))

        return True

    def __str__(self):
        regla = f"   {('0 1 2 3 4 5 6 7 8 9 ' * int (self.dimension / 10 + 1))[:self.dimension * 2]}\n"
        linea = regla
        for i in range(self.dimension):
            linea += f"{i:2d} {' '.join(self.matriz[i].tolist())} {i:2d}\n"
        return linea + regla


import pygame
import numpy as np
import random

palabras = ["arqui", "compu", "emular", "proc", "nucleo", "chip", "buffer"]
TAM = 10
matriz = Matrix(TAM)
while matriz.libres:
    palabra = palabras[random.randint(0, len(palabras) - 1)]
    largo = len(palabra)
    matriz.put(palabra)

#MUESTRA EN TERMINAL
print(matriz)
print(matriz.palabras)

pygame.init()
width, height = 1250, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sopa de Letras")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

cell_size = 55
margin = 10
board_width = matriz.dimension * cell_size
board_height = matriz.dimension * cell_size
board_x = (width - board_width) // 2 - 100
board_y = (height - board_height) // 2

# Inicializar la matriz de botones seleccionados
boton_seleccionado = [[False] * TAM for _ in range(TAM)]
boton_encontrado = [[False] * TAM for _ in range(TAM)]

mensaje_mostrado = " "
palabras_mostradas = "Palabras aquí"
palabras_buscadas = []
palabra_encontrada = ""
tiempo_transcurrido = 0
max_tiempo = 180


def texto_palabras():
    txt_palabras = ""
    
    for palabra in palabras_buscadas:
        palabra_texto = palabra
        txt_palabras += palabra_texto + "\n"
        
    txt_palabras += "Encuentra las palabras:"

    return txt_palabras


def comprobar_palabras(botones_seleccionados):
    encontrado = False
    for palabra in matriz.palabras:
        x, y, avanX, avanY, palabra_texto = palabra
        x1 = x
        y1 = y
        x2 = x1 + avanX * len(palabra_texto) - avanX
        y2 = y1 + avanY * len(palabra_texto) - avanY

        boton1 = botones_seleccionados[0]
        boton2 = botones_seleccionados[1]

        if boton1 == (x1, y1) and boton2 == (x2, y2):
            encontrado = True
        if boton1 == (x2, y2) and boton2 == (x1, y1):
            encontrado = True        

    return encontrado


def aceptar_palabra(botones_seleccionados):
    global palabras_buscadas
    global palabras_mostradas
    global palabra_encontrada
    
    boton1 = botones_seleccionados[0]
    boton2 = botones_seleccionados[1]
    x1 = boton1[0]
    y1 = boton1[1]
    x2 = boton2[0]
    y2 = boton2[1]
    
    boton_encontrado[x1][y1] = True
    boton_encontrado[x2][y2] = True

    palabra_encontrada = matriz[Cursor(x1, y1)]
    
    if x1 == x2:
        for y in range(y1+1, y2):
            boton_encontrado[x1][y] = True
            palabra_encontrada += matriz[Cursor(x1, y)]
            
    elif y1 == y2:
        for x in range(x1+1, x2):
            boton_encontrado[x][y1] = True
            palabra_encontrada += matriz[Cursor(x, y1)]
    
    elif abs(x2 - x1) == abs(y2 - y1):
        dx = 1 if x2 > x1 else -1
        dy = 1 if y2 > y1 else -1
        x = x1 + dx
        y = y1 + dy
        while x != x2:
            boton_encontrado[x][y] = True
            palabra_encontrada += matriz[Cursor(x, y)]
            x += dx
            y += dy

    palabra_encontrada += matriz[Cursor(x2, y2)]
    
    boton_seleccionado[x1][y1] = False
    boton_seleccionado[x2][y2] = False
    
    print(palabra_encontrada)
    if palabra_encontrada in palabras_buscadas:
        palabras_buscadas.remove(palabra_encontrada)
    else:
        palabra_encontrada = palabra_encontrada[::-1]
        if palabra_encontrada in palabras_buscadas:
            palabras_buscadas.remove(palabra_encontrada)
    palabras_mostradas = texto_palabras()

    return palabra_encontrada


def draw_board():
    global mensaje_mostrado
    global palabras_mostradas
    
    # Mostrar temporizador en la parte superior izquierda
    tiempo_restante = int(max_tiempo - tiempo_transcurrido)
    tiempo_restante = max(0, tiempo_restante)
    tiempo_texto = f"Tiempo: {tiempo_restante} s"
    tiempo_rect = pygame.Rect(10, 10, 200, 30)
    pygame.draw.rect(screen, WHITE, tiempo_rect)
    pygame.draw.rect(screen, BLACK, tiempo_rect, 1)
    font = pygame.font.Font(None, 24)
    text = font.render(tiempo_texto, True, BLACK)
    text_rect = text.get_rect(center=tiempo_rect.center)
    screen.blit(text, text_rect)

    # Mostrar números de fila en el borde superior
    for columna in range(matriz.dimension):
        rect = pygame.Rect(board_x + columna * cell_size, board_y - cell_size, cell_size, cell_size)
        font = pygame.font.Font(None, 24)
        text = font.render(str(columna), True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    # Mostrar números de columna en el borde izquierdo
    for fila in range(matriz.dimension):
        for columna in range(matriz.dimension):
            letra = matriz[Cursor(fila, columna)]
            rect = pygame.Rect(board_x + columna * cell_size, board_y + fila * cell_size, cell_size, cell_size)
            
            # Crear un botón interactivo
            button_color = WHITE
            if boton_encontrado[fila][columna]: button_color = GREEN
            if boton_seleccionado[fila][columna]: button_color = BLUE
            
            button = pygame.draw.rect(screen, button_color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            
            font = pygame.font.Font(None, 24)
            text = font.render(letra, True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    # Dibujar el botón de verificación
    verificacion_rect = pygame.Rect(screen.get_width() - 140, screen.get_height() - 50, 120, 30)
    verificacion_button = pygame.draw.rect(screen, GREEN, verificacion_rect)
    font = pygame.font.Font(None, 24)
    text = font.render("Verificar", True, BLACK)
    text_rect = text.get_rect(center=verificacion_rect.center)
    screen.blit(text, text_rect)

    # Dibujar el apartado de texto editable
    texto_rect = pygame.Rect(screen.get_width() // 2 - 300, screen.get_height() - 50, 600, 30)
    pygame.draw.rect(screen, WHITE, texto_rect)
    pygame.draw.rect(screen, BLACK, texto_rect, 1)
    font = pygame.font.Font(None, 24)
    text = font.render(mensaje_mostrado, True, BLACK)
    text_rect = text.get_rect(center=texto_rect.center)
    screen.blit(text, text_rect)

    # Dibujar el apartado de las palabra
    texto_rect = pygame.Rect(screen.get_width() - 300, screen.get_height() // 2 - 250, 260, 500)
    pygame.draw.rect(screen, WHITE, texto_rect)
    pygame.draw.rect(screen, BLACK, texto_rect, 1)
    font = pygame.font.Font(None, 24)
    line_height = font.get_linesize() + 10
    # Dibujar cada línea de palabra
    palabras_lineas = palabras_mostradas.splitlines()
    for i, linea in enumerate(palabras_lineas):
        text = font.render(linea, True, BLACK)
        text_rect = text.get_rect(center=(texto_rect.centerx, texto_rect.centery - i * line_height + line_height * len(palabras_lineas) // 2))
        screen.blit(text, text_rect)
    
    # Obtener eventos de pygame
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar si se hizo clic en un botón
            mouse_pos = pygame.mouse.get_pos()
            for fila in range(matriz.dimension):
                for columna in range(matriz.dimension):
                    rect = pygame.Rect(board_x + columna * cell_size, board_y + fila * cell_size, cell_size, cell_size)
                    if rect.collidepoint(mouse_pos):
                        # Cambiar el estado del botón seleccionado
                        boton_seleccionado[fila][columna] = not boton_seleccionado[fila][columna]

            # Verificar si se hizo clic en el botón de verificación
            if verificacion_rect.collidepoint(mouse_pos):
                # Realizar la verificación de los botones seleccionados
                botones_seleccionados = []
                for fila in range(matriz.dimension):
                    for columna in range(matriz.dimension):
                        if boton_seleccionado[fila][columna]:
                            botones_seleccionados.append((fila, columna))
                print("Botones seleccionados:", botones_seleccionados)
                
                if len(botones_seleccionados) == 2:
                    if comprobar_palabras(botones_seleccionados):
                        mensaje_mostrado = "Encontró una palabra" + aceptar_palabra(botones_seleccionados)
                    else:
                        mensaje_mostrado = "Es incorrecto, intente de nuevo"                        
                else:
                    mensaje_mostrado = "Por favor seleccione solo el inicio y final de la palabra"

    for fila in range(matriz.dimension):
        rect = pygame.Rect(board_x - cell_size, board_y + fila * cell_size, cell_size, cell_size)
        font = pygame.font.Font(None, 24)
        text = font.render(str(fila), True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)


draw_board()
for palabra in matriz.palabras:
    palabras_buscadas.append(palabra[4])
palabras_mostradas = texto_palabras()

running = True
while running:
    screen.fill(WHITE)
    tiempo_transcurrido += clock.tick(60) / 1000
    draw_board()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
