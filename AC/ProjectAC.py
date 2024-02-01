import pyttsx3 as con
from openai import OpenAI
import speech_recognition as reconoce
import json
import os
import cv2

#KEY API
client = OpenAI(api_key ='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')

#CONVERT
convert = reconoce.Recognizer()

#CONVIERTE EN AUDIO, LAS CADENAS DE TEXTO
def STAU (ingreso):
    palabra = con.init()
    palabra.setProperty('rate',150)
    palabra.setProperty('voice', 'Spanish (Latin America)')
    palabra.say(ingreso)
    palabra.runAndWait()

#PETICIONES DIFERENTES
def CUE (quetion):
    answer = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": quetion}]
    )
    #answer = openai.Completion.create(
    #        engine = "text-davinci-002",
    #        prompt = quetion,
    #        max_tokens = 100,
    #        temperature = 0.6
    #        )
    return answer.choices[0].message.content
    
#RECONOCE LA VOZ
def VOZ (tipo):
    with reconoce.Microphone() as sr:
        #if(valor):
        #    STAU ('PORFAVOR INGRESE SU PETICIÓN')
        #else:
        #    STAU ('POR FAVOR COMENTE SU RESPUESTA')
        STAU ('PORFAVOR INGRESE SU ' + tipo)
        song = convert.listen(sr)
        STAU ('OKEY EN PROCESO')
    
    try:
        text_song = convert.recognize_google(song)
        STAU('SU '+ tipo +' SE HA TRANSCRITO EN LA TERMINAL')
        print ('SU '+ tipo +': ', text_song)
        return text_song
    except reconoce.UnknownValueError:
        STAU('No se reconoce correctamente su peticion por audio')
    except reconoce.RequestError as e:
        print("Error en la solicitud a Google Speech Recognition: {0}".format(e))

#ENLACE BASE DE DATOS
#with open('DATA.json', 'r') as archivo:
#    datos =  json.load(archivo)

#MAIN: FUNCION PRINCIPAL
if __name__ == "__main__":
    print(CUE('NO EXPLIQUES NADA SOLO DAME EN LIMPIO LA REPSUESTA,una pregunta de Arquitectura de computadoras en json con sus alternativas, y su respuesta como esto:{"pregunta": "¿Cuál es la capital de Francia?", "alternativas": ["Londres", "París", "Berlín", "Madrid"],  "respuesta": "París"}'))	
    #SALUDO
    #STAU(datos['welcome'])
    
    #PIDE NOMBRE
    #nombre = VOZ('nombre')
    #print ('Tu nombre es: ', nombre)
    
    #PREGUNTA LA ELECCION
    #eleccion = VOZ('elección')
    #print ('Usted elijió: ', eleccion)
    #if eleccion == None:
    #    os.system('python ./HM/HMV2.py & python sopa.py') #Ejecutar a la vez (linux)

    #DESPEDIDA
    #STAU(datos['later'])
