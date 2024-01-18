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


import numpy as np
import random

palabras = ["arqui", "compu", "emular", "proc", "nucleo", "chip", "buffer"]
TAM = 15
matriz = Matrix(TAM)
while matriz.libres:
    palabra = palabras[random.randint(0, len(palabras) - 1)]
    largo = len(palabra)
    matriz.put(palabra)

print(matriz)
print(matriz.palabras)
