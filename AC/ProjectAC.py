import pyttsx3 as con
import json
#CONVIERTE EN AUDIO, LAS CADENAS DE TEXTO
def STAU (ingreso):
    palabra = con.init()
    palabra.setProperty('rate',150)
    palabra.say(ingreso)
    palabra.runAndWait()
#ENLACE BASE DE DATOS
with open('DATA.json', 'r') as archivo:
    datos =  json.load(archivo)

#MAIN: FUNCION PRINCIPAL
if __name__ == "__main__":
    STAU(datos['welcome'])
