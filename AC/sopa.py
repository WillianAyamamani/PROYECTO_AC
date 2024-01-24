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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

cell_size = 55
margin = 10
board_width = matriz.dimension * cell_size
board_height = matriz.dimension * cell_size
board_x = (width - board_width) // 2
board_y = (height - board_height) // 2

# Inicializar la matriz de botones seleccionados
boton_seleccionado = [[False] * TAM for _ in range(TAM)]
boton_encontrado = [[False] * TAM for _ in range(TAM)]

mensaje_mostrado = " "

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

def draw_board():
    global mensaje_mostrado

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
    texto_rect = pygame.Rect(screen.get_width() // 2 - 300, screen.get_height() - 40, 600, 30)
    pygame.draw.rect(screen, WHITE, texto_rect)
    pygame.draw.rect(screen, BLACK, texto_rect, 1)
    font = pygame.font.Font(None, 24)
    text = font.render(mensaje_mostrado, True, BLACK)
    text_rect = text.get_rect(center=texto_rect.center)
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
                        mensaje_mostrado = "Encontró una palabra"
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

running = True
while running:
    screen.fill(WHITE)
    draw_board()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
