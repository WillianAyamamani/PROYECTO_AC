import pyttsx3 as con
from openai import OpenAI
import json
import os
import cv2
from flask import Flask, render_template, request
import webbrowser

#KEY API
client = OpenAI(api_key ='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')

#PETICIONES DIFERENTES
def CUE (quetion):
    answer = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": quetion}]
    )
    return answer.choices[0].message.content
    
#APLICACION DE FLASK
app = Flask(__name__)
@app.route("/Asistente")
def HOME():
    return render_template('Asistente.html')

@app.route("/Asistente", methods=['POST'])
def Question():
    pregunta = request.form['pregunta']
    respuest = CUE(pregunta)
    return render_template('Asistente.html', prueba = pregunta, resp = respuest)

#MAIN: FUNCION PRINCIPAL
if __name__ == "__main__":
    webbrowser.open_new('http://127.0.0.1:5000/Asistente')
    app.run()

    #print(CUE('NO EXPLIQUES NADA SOLO DAME EN LIMPIO LA REPSUESTA,una pregunta de Arquitectura de computadoras en json con sus alternativas, y su respuesta como esto:{"pregunta": "¿Cuál es la capital de Francia?", "alternativas": ["Londres", "París", "Berlín", "Madrid"],  "respuesta": "París"}'))	
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
