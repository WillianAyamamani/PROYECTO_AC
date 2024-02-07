from flask import Flask, render_template, request
from ProjectAC import CUE
import json
import webbrowser
#CONECTION::CHATGPT

#TEST::FUNTION::ASISTENT
app = Flask(__name__)
#::::::::::::::::::::::::::::::#
#ESTRUCTURA:
#---------------#
#HOME
#PERFIL
#ABOUT
#---------------#
#HOME:
##NIVELES
##SIMULACRO
##DOCUMENTACION
#---------------#
#ABOUT
##CONOCIMIENTO_DE_LOS CREADORES
#---------------#
#PERFIL
##PORCENTAJE_PROGRESO
##NOMBRE
##TEMAS
#---------------#
##NIVELES:
###EASY
###HARD
###VERY HARD
#:::::::::::::::::::::::::::::#

#HOME == PAGINA PRINCIPAL
@app.route("/")
def HOME():
    #Creacion de nuevas preguntas
    prompt = 'RESPUESTA LIMPIA, NO EXPLIQUES NADA, Genera un formato json dame 10 preguntas (sin signos de interregacion y sin mayusculas, no pongas la tilde de las palabras) acerca de arquitectura de computadoras con 4 alternativas y su alternativa correcta, (es OBLIGATORIO que este sin signos de interregacion y sin mayusculas, no pongas la tilde de las palabras, en toda la RESPUESTA"), Example: "{    "preguntas": [        {            "pregunta": "que es la arquitectura de computadoras?",            "alternativas": ["conjunto de componentes de hardware y software que conforman un sistema de computación", "conjunto de programas de computadora", "conjunto de lenguajes de programación", "conjunto de periféricos de entrada y salida"],            "alternativaCorrecta": "conjunto de componentes de hardware y software que conforman un sistema de computacion"        },        {            "pregunta": "que es la unidad central de procesamiento (cpu)?",            "alternativas": ["memoria de almacenamiento interno", "dispositivo de entrada de información", "dispositivo de salida de información", "componente principal que realiza las operaciones y controla el funcionamiento del sistema"],            "alternativaCorrecta": "componente principal que realiza las operaciones y controla el funcionamiento del sistema"},"'

    question=CUE(prompt)
    print(question)
    que = json.loads(question)
    
    with open ('prueba.json','w') as page:
        json.dump(que, page, indent = 6) 

    return render_template('index.html')

#USER == PERFIL DEL USUARIO
@app.route("/Users")
def PERFIL():
    return render_template('profile.html')

#ASISTENT == CONOCIMIENTO DEL PROGRAMA
@app.route("/ASISTENT")
def ABOUT():
    return render_template('about.html')

#EXAMEM == DESICION DEL TEST

@app.route("/examen")
def TEST():
    #  :::FALTA:::
    with open('prueba.json', 'r', encoding = 'utf-8') as file:
        datos = json.load(file)
    preguntas = datos.get("preguntas",[])
    total = datos.get("total")
    print(total)
    #preguntas = json.get_json('prueba.json')
    #preguntas = {"preguntas": [{"texto": generated_json_str, "alternativas": []}]}

    return render_template('examen.html', preguntas=preguntas, total = total)
    #   :::**:::
    #return render_template('index.html')

if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run()
