from flask import Flask, render_template
import json
import webbrowser

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
    preguntas_data = {
        "preguntas": [
            {
                "texto": "¿Cuál es el primer científico?",
                "alternativas": ["Aristóteles", "Galileo Galilei", "Isaac Newton", "Arquímedes"]
            },
            {
                "texto": "Otra pregunta",
                "alternativas": ["Opción 1", "Opción 2", "Opción 3"]
            },
            {
                "texto": "Y otra más",
                "alternativas": ["Respuesta A", "Respuesta B", "Respuesta C"]
            }
        ]
    }

    # Parse the JSON data
    json_data = json.dumps(preguntas_data)
    preguntas = json.loads(json_data)

    return render_template('examen.html', preguntas=preguntas)

if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run()
