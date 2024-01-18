import pyttsx3 as con
import openai
import speech_recognition as reconoce
import json
import os

#KEY API
openai.api_key = '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'

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
    answer = openai.Completion.create(
            engine = "text-davinci-002",
            prompt = quetion,
            max_tokens = 100,
            temperature = 0.6
            )
    return answer['choices'][0]['text']
    
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
with open('DATA.json', 'r') as archivo:
    datos =  json.load(archivo)

#MAIN: FUNCION PRINCIPAL
if __name__ == "__main__":
    #SALUDO
    #STAU(datos['welcome'])
    
    #PIDE NOMBRE
    nombre = VOZ('nombre')
    print ('Tu nombre es: ', nombre)
    
    #PREGUNTA LA ELECCION
    eleccion = VOZ('elección')
    print ('Usted elijió: ', eleccion)
    if eleccion == 'Uno':
        os.system('python sopa.py')    

    #DESPEDIDA
    #STAU(datos['later'])